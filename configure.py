import json
import codecs
import enum
import hashlib
from functools import reduce
from itertools import product


class Config:
    version = "1.0.3"
    fontRevision = 1 + 0x0003 / 0x10000
    vendor = "Nowar Typeface"
    vendorId = "NOWR"
    vendorUrl = "https://github.com/nowar-fonts"
    copyright = "Copyright © 2018—2022 Cyano Hao and Nowar Typeface, with Reserved Font Name “Nowar”, “Новар”, “Νοωαρ”, “有爱”, and “有愛”. Portions Copyright 2015 Google LLC.. Portions © 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'."
    designer = "Cyano Hao (character set definition & modification for World of Warcraft); Monotype Design Team (Latin, Greek & Cyrillic); Ryoko NISHIZUKA 西塚涼子 (kana, bopomofo & ideographs); Sandoll Communications 산돌커뮤니케이션, Soo-young JANG 장수영 & Joo-yeon KANG 강주연 (hangul elements, letters & syllables); Dr. Ken Lunde (project architect, glyph set definition & overall production); Masataka HATTORI 服部正貴 (production & ideograph elements)"
    designerUrl = "https://github.com/CyanoHao"
    license = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This Font Software is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the SIL Open Font License for the specific language, permissions and limitations governing your use of this Font Software."
    licenseUrl = "https://scripts.sil.org/OFL"

    fontPackWeight = [300, 350, 400, 450, 500, 600, 700]
    fontPackRegion = [
        "Bliz", "Neut", "CL",
        "Pinyin", "Pinyin,Romaja", "Romaja",
    ]
    fontPackFeature = ["CyR", "OSF", "RP", "SC"]
    # feature tags must be sorted alphabetically
    fontPackExportFeature = [
        ("Neut", ["CyR"]),
        ("Pinyin", ["CyR"]),
        ("Pinyin,Romaja", ["CyR"]),
        ("Romaja", ["CyR"]),
    ]

    globalFontWeight = [300, 400, 500, 600, 700]
    globalFontInstance = [
        ("gbk", "CN", [], 3),
        ("gbk", "CN", [], 5),
        ("big5", "TW", [], 3),
        ("big5", "TW", [], 5),
        ("unspec", "CL", ["UI"], 3),
        ("unspec", "CL", ["UI"], 7),
    ]


config = Config()


# define Chinese characters orthographies, and feature mods:
#
# base - common fonts, `FRIZQT__` and `ARIALN`; must be defined
# enUS - fonts for languages in Latin script, `skurri` and `MORPHEUS`
#        if set to something to be true, the orthography is considered to be same as `base`
#        if set to something to be false, fonts will be not overwritten
# ruRU - fonts for Русский; like `enUS`
# zhCN - fonts for 简体中文; can be false
# zhTW - fonts for 繁體中文; can be false
# koKR - fonts for 한국어; can be false
#
# xmod - a list of tuples of feature mod and related parameter list
# available mods:
#   PSimp - 伪简体, remap traditional Chinese characters to simplified ones in zhTW text, damage, and note font
#     base - also do remapping in common fonts (`FRIZQT__` and `ARIALN`)
#     chat - also do remapping in zhTW chat fonts (`arheiuhk_bd` for Battle and `bHEI01B` for Classic)
#   Pinyin - transcription of Chinese characters in Hànyǔ Pīnyīn (汉语拼音), will not do transform in zhCN/zhTW fonts
#   Romaja - transcription of Hanguel in revised romanization of korean (국어의 로마자 표기법), will not do transform in koKR fonts
regionalVariant = {
    "Neut": {
        "base": "CL",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CN",
        "zhTW": "TW",
        "koKR": "CL",
    },
    "Bliz": {
        "base": "CN",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CN",
        "zhTW": "TW",
        "koKR": "CN",  # yes, it is
    },
    "CL": {
        "base": "CL",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CL",
        "zhTW": "CL",
        "koKR": "CL",
    },
    "PSimp": {
        "base": "CN",
        "enUS": None,
        "ruRU": None,
        "zhCN": None,
        "zhTW": "CN",
        "koKR": None,
        "xmod": [("PSimp", ["base"])],
    },
    "PSimpChat": {
        "base": "CN",
        "enUS": None,
        "ruRU": None,
        "zhCN": None,
        "zhTW": "CN",
        "koKR": None,
        "xmod": [("PSimp", ["base", "chat"])],
    },
    "Pinyin": {
        "base": "CL",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CN",
        "zhTW": "TW",
        "koKR": "CL",
        "xmod": [("Pinyin", [])],
    },
    "Pinyin,Romaja": {
        "base": "CL",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CN",
        "zhTW": "TW",
        "koKR": "CL",
        "xmod": [("Pinyin", []), ("Romaja", [])],
    },
    "Romaja": {
        "base": "CL",
        "enUS": True,
        "ruRU": True,
        "zhCN": "CN",
        "zhTW": "TW",
        "koKR": "CL",
        "xmod": [("Romaja", [])],
    },
}


class LanguageId(enum.IntEnum):
    enUS = 0x0409


weightMap = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    350: "SemiLight",
    372: "Normal",
    400: "",
    450: "Book",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}

weightMapShort = {
    100: "Th",
    200: "XLt",
    300: "Lt",
    350: "SmLt",
    372: "Nm",
    400: "",
    450: "Bk",
    500: "Md",
    600: "SmBd",
    700: "Bd",
    800: "XBd",
    900: "Blk",
}

widthMap = {
    3: "Condensed",
    4: "SemiCondensed",
    5: None,
    7: "Extended",
    10: "Warcraft",  # Warcraft numeral hack
}

widthMapShort = {
    3: "Cn",
    4: "SmCn",
    5: None,
    7: "Ex",
    10: "Wc",
}

slantMapShort = {
    "Italic": "It",
    "Oblique": "Obl",
}

notoWidthMap = {
    3: 75,
    5: 87.5,
    7: 100,
}


def AxisMapNotoWgth(wght: float) -> float:
    # map user value to normalized design space.
    # the original definition for 400 -- 900 is almost linear, simply use linear interpolation.
    # 100 .. -1
    # 200 .. -0.8
    # 300 .. -0.5
    # 400 ..  0
    # 900 ..  1
    if wght < 100:
        return -1
    if wght <= 200:
        return -1 + (wght - 100) / 100 * 0.2
    if wght <= 300:
        return -0.8 + (wght - 200) / 100 * 0.3
    if wght <= 400:
        return -0.5 + (wght - 300) / 100 * 0.5
    if wght <= 900:
        return (wght - 400) / 500
    return 1


def AxisMapNotoWdth(wdth: float) -> float:
    # map user value to normalized design space.
    # the original definition for 75 -- 100 is almost linear, simply use linear interpolation.
    #  62.5 .. -1
    #  75   .. -0.7
    # 100   ..  0
    if wdth < 62.5:
        return -1
    if wdth <= 75:
        return -1 + (wdth - 62.5) / 12.5 * 0.3
    if wdth <= 100:
        return -0.7 + (wdth - 75) / 25 * 0.7
    return 0


def AxisMapShsWght(wght: float) -> float:
    # map user value to normalized design space.
    # adjusted to match our definition for Noto Sans
    # 200 .. 0
    # 300 .. 0.15
    # 400 .. 0.4
    # 900 .. 1
    if wght < 200:
        return 0
    if wght <= 300:
        return (wght - 200) / 100 * 0.15
    if wght <= 400:
        return 0.15 + (wght - 300) / 100 * 0.25
    if wght <= 900:
        return 0.4 + (wght - 400) / 500 * 0.6
    return 1


# map orthography to source file
shsRegionMap = {
    "CN": "SourceHanSansSC",
    "TW": "SourceHanSansTC",
    "HK": "SourceHanSansHC",
    "MO": "SourceHanSansMC",
    "JP": "SourceHanSans",
    "KR": "SourceHanSansK",
    "CL": "SourceHanSansK",
}

regionNameMap = {
    "CN": "CN",
    "TW": "TW",
    "HK": "HK",
    "MO": "MO",
    "JP": "JP",
    "KR": "KR",
    "CL": "Classical",
}

# sorted alphabetically
featureNameMap = {
    "CyR": "Cyrillic-Romanisation",
    "FuCK": "Fullwidth-Colon-Kerning",
    "OSF": "Oldstyle",
    "Pinyin": "Pinyin",
    "RP": "Roleplaying",
    "Romaja": "Romaja",
    "SC": "Smallcaps",
    "Simp": "Simplified",
    "UI": "UI",
}

tagNameMap = {**regionNameMap, **featureNameMap}


def LocalizedFamily(p):
    if "nameList" not in LocalizedFamily.__dict__:
        LocalizedFamily.nameList = {
            LanguageId.enUS: "Dragonflight Sans",
        }
    return LocalizedFamily.nameList


def TagListToStr(lst):
    return ",".join(lst)


def GenerateFontName(p):
    localizedFamily = LocalizedFamily(p)
    region = p["region"]
    feature = [*sorted(p["feature"])]

    regionName = regionNameMap[region]
    subfamily = [tagNameMap[fea] for fea in feature]
    filenameSf = []
    wwsF = [region, *feature]
    wwsSf = []
    legacyF = [region, *feature]
    legacySf = []

    width = p["width"]
    widthName = widthMap[width]
    widthShort = widthMapShort[width]
    if widthName:
        subfamily.append(widthName)
        filenameSf.append(widthName)
        legacyF.append(widthShort)
    # Warcraft numeral hack
    if width == 10:
        wwsF.append(widthShort)
    elif widthName:
        wwsSf.append(widthName)

    weight = p["weight"]
    weightName = weightMap[weight] if weight in weightMap else f"W{weight}"
    weightShort = weightMapShort[weight] if weight in weightMapShort else f"W{weight}"
    if weightName:
        subfamily.append(weightName)
        filenameSf.append(weightName)
        wwsSf.append(weightName)
        if weight == 700:
            legacySf.append(weightName)
        else:
            legacyF.append(weightShort)

    if p.get("slant"):
        slantName = p["slant"]
        slantShort = slantMapShort[slantName]
        subfamily.append(slantName)
        filenameSf.append(slantName)
        wwsSf.append(slantName)
        if slantName == "Italic":
            legacySf.append(slantName)
        else:
            legacyF.append(slantShort)

    def formatFamily(f):
        return " ".join(f)

    def formatSubfamily(sf):
        return " ".join(sf) or "Regular"

    subfamily = formatSubfamily(subfamily)
    filenameF = localizedFamily[LanguageId.enUS].replace(" ", "")
    filenameTag = TagListToStr([p["region"], *sorted(p["feature"])])
    filenameSf = formatSubfamily(filenameSf).replace(" ", "")
    wwsF = formatFamily(wwsF)
    wwsSf = formatSubfamily(wwsSf)
    legacyF = formatSubfamily(legacyF)
    legacySf = formatSubfamily(legacySf)

    return {
        "typographic": ({k: "{} {}".format(v, regionName) for k, v in localizedFamily.items()}, subfamily),
        "wws": ({k: "{} {}".format(v, wwsF) for k, v in localizedFamily.items()}, wwsSf),
        "legacy": ({k: "{} {}".format(v, legacyF) for k, v in localizedFamily.items()}, legacySf),
        "friendly": {k: "{} {} {}".format(v, regionName, subfamily) for k, v in localizedFamily.items()},
        "file": "{}-{}-{}".format(filenameF, filenameTag, filenameSf),
        # font name can be too long to fit in 63-char PostScript name
        # the hashed name makes no sence but is valid
        "postscript": filenameF + "-" + hashlib.sha1("{} {}".format(regionName, subfamily).encode()).hexdigest(),
    }


def GenerateFilename(p):
    if p["family"] == "Nowar":
        filename = GenerateFontName(p)["file"]
        return p["encoding"] + "-" + filename
    elif p["family"] == "Noto":
        return f"NotoSans-wght{p['weight']}wdth{p['width']}"
    else:  # SHS
        return f"{p['region']}-wght{p['weight']}"


def ResolveDependency(p):
    if p["width"] == 10:  # Warcraft numeral hack
        result = {
            "Latin": {
                "family": "Noto",
                "width": 87.5,
                "weight": p["weight"],
            },
            "Numeral": {
                "family": "Noto",
                "width": 75,
                "weight": p["weight"],
            },
        }
    else:
        result = {
            "Latin": {
                "family": "Noto",
                "width": notoWidthMap[p["width"]],
                "weight": p["weight"],
            },
        }
    if "Pinyin" in p["feature"] or "Romaja" in p["feature"]:
        result['Roman'] = {
            "family": "Noto",
            "width": 75,
            "weight": p["weight"],
        }
    result["CJK"] = {
        "family": "SHS",
        "weight": p["weight"],
        "region": shsRegionMap[p["region"]],
    }
    return result


def AcceptXmod(region, pinyin=False, romaja=False, pSimp=[]):
    xfea = []
    for mod, params in regionalVariant[region].get("xmod", []):
        if pinyin and mod == "Pinyin":
            xfea.append("Pinyin")
        if romaja and mod == "Romaja":
            xfea.append("Romaja")
        if (pSimp is True and mod == "PSimp") or (mod == "PSimp" and any(key in params for key in pSimp)):
            xfea.append("Simp")
    return xfea


def GetCommonFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True, romaja=True, pSimp=["base"])
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "unspec",
    }


def GetCommonChatFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True, romaja=True, pSimp=["base"])
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "unspec",
    }


def GetLatinFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True, romaja=True)
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "abg",
    }


def GetLatinChatFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True, romaja=True)
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "abg",
    }


def GetHansFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True)
    return {
        "weight": weight,
        "width": 10,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": ["FuCK"] + feature + xfea,
        "encoding": "gbk",
    }


def GetHansCombatFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True)
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": feature + xfea,
        "encoding": "gbk",
    }


def GetHansChatFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True)
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": feature + xfea,
        "encoding": "gbk",
    }


def GetHantFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True, pSimp=True)
    return {
        "weight": weight,
        "width": 10,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantCombatFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True, pSimp=True)
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantNoteFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True, pSimp=True)
    return {
        "weight": weight,
        "width": 5,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantChatFont(weight, region, feature):
    xfea = AcceptXmod(region, romaja=True, pSimp=["chat"])
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetKoreanFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True)
    return {
        "weight": weight,
        "width": 5,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "korean",
    }


def GetKoreanCombatFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True)
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "korean",
    }


def GetKoreanDisplayFont(weight, region, feature):
    xfea = AcceptXmod(region, pinyin=True)
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "korean",
    }


def ParamToArgument(param):
    js = json.dumps(param, separators=(',', ':'))
    return "'{}'".format(js)


if __name__ == "__main__":
    makefile = {
        "variable": {
            "VERSION": config.version,
        },
        "rule": {
            ".PHONY": {
                "depend": ["all", "GlobalFont", "NamingTest"],
            },
            "all": {
                "depend": [],
            },
            "GlobalFont": {
                "depend": [],
            },
            "NamingTest": {
                "depend": [],
            },
            "clean": {
                "command": [
                    "-rm -rf build/",
                    "-rm -rf out/??*-???/",
                ]
            }
        },
    }

    def powerset(lst): return reduce(lambda result, x: result +
                                     [subset + [x] for subset in result], lst, [[]])

    finalOtfDeps = set()
    nowarOtdDeps = set()

    # font pack for each regional variant and weight
    for r, w, fea in product(config.fontPackRegion, config.fontPackWeight, powerset(config.fontPackFeature)):
        tagList = [r] + fea
        target = "{}-{}".format(TagListToStr(tagList), w)
        pack = "out/DragonflightSans-{}-${{VERSION}}.7z".format(target)

        makefile["rule"][".PHONY"]["depend"].append(target)
        makefile["rule"][target] = {
            "depend": [pack],
        }

        if fea == [] or (r, fea) in config.fontPackExportFeature:
            makefile["rule"]["all"]["depend"].append(pack)

        fontlist = {
            "ARIALN": GetCommonChatFont(w, r, fea),
            "FRIZQT__": GetCommonFont(w, r, fea),
        }

        if regionalVariant[r]["enUS"]:
            fontlist.update({
                "skurri": GetLatinFont(w, r, fea),
                "MORPHEUS": GetLatinChatFont(w, r, fea),
            })

        if regionalVariant[r]["ruRU"]:
            fontlist.update({
                "FRIZQT___CYR": GetLatinFont(w, r, fea),
                "SKURRI_CYR": GetLatinFont(w, r, fea),
                "MORPHEUS_CYR": GetLatinChatFont(w, r, fea),
            })

        if regionalVariant[r]["zhCN"]:
            fontlist.update({
                "ARKai_C": GetHansCombatFont(w, r, fea),
                "ARKai_T": GetHansFont(w, r, fea),
                "ARHei": GetHansChatFont(w, r, fea),
            })

        if regionalVariant[r]["zhTW"]:
            fontlist.update({
                "arheiuhk_bd": GetHantChatFont(w, r, fea),
                "bHEI00M": GetHantNoteFont(w, r, fea),
                "bHEI01B": GetHantChatFont(w, r, fea),
                "bKAI00M": GetHantCombatFont(w, r, fea),
                "blei00d": GetHantFont(w, r, fea),
            })

        if regionalVariant[r]["koKR"]:
            fontlist.update({
                "2002": GetKoreanFont(w, r, fea),
                "2002B": GetKoreanFont(w, r, fea),
                "K_Damage": GetKoreanCombatFont(w, r, fea),
                "K_Pagetext": GetKoreanDisplayFont(w, r, fea),
            })

        finalOtfDeps.update(map(json.dumps, fontlist.values()))

        makefile["rule"][pack] = {
            "depend": ["out/{}/Fonts/{}.ttf".format(target, f) for f in fontlist],
            "command": [
                f"cd out/{target};" +
                "cp ../../LICENSE.txt Fonts/LICENSE.txt;" +
                "7z a -t7z -m0=LZMA:d=512m:fb=273 -ms ../../$@ Fonts/"
            ]
        }

        for f, p in fontlist.items():
            makefile["rule"]["out/{}/Fonts/{}.ttf".format(target, f)] = {
                "depend": ["build/final-otf/{}.otf".format(GenerateFilename(p))],
                "command": [
                    "mkdir -p out/{}/Fonts".format(target),
                    "cp $^ $@",
                ]
            }

    # font files for Global Font addon
    for w, (e, r, fea, wd) in product(config.globalFontWeight, config.globalFontInstance):
        param = {
            "family": "Nowar",
            "weight": w,
            "width": wd,
            "region": r,
            "feature": fea,
            "encoding": e,
        }
        font = "out/GlobalFont/{}.otf".format(
            GenerateFilename(param)[len(e)+1:])

        finalOtfDeps.add(json.dumps(param))
        makefile["rule"]["GlobalFont"]["depend"].append(font)
        makefile["rule"][font] = {
            "depend": ["build/final-otf/{}.otf".format(GenerateFilename(param))],
            "command": [
                "mkdir -p out/GlobalFont/",
                "cp $^ $@",
            ]
        }

    # naming test
    for w, r, wd, fea in product(config.globalFontWeight, ["CN", "CL"], [3, 5, 7], [[], ["UI", "OSF", "SC", "RP", "Simp"]]):
        param = {
            "family": "Nowar",
            "weight": w,
            "width": wd,
            "region": r,
            "feature": fea,
            "encoding": "unspec",
        }
        font = "out/NamingTest/{}.otf".format(
            GenerateFilename(param)[len(e)+1:])

        finalOtfDeps.add(json.dumps(param))
        makefile["rule"]["NamingTest"]["depend"].append(font)
        makefile["rule"][font] = {
            "depend": ["build/final-otf/{}.otf".format(GenerateFilename(param))],
            "command": [
                "mkdir -p out/NamingTest/",
                "cp $^ $@",
            ]
        }

    # resolve deps -- final otf
    for param in finalOtfDeps:
        param = json.loads(param)
        makefile["rule"]["build/final-otf/{}.otf".format(GenerateFilename(param))] = {
            "depend": ["build/unkerned-otf/{}.otf".format(GenerateFilename(param))],
            "command": [
                "mkdir -p build/final-otf/",
                "python kern.py {}".format(ParamToArgument(param)),
            ],
        }
        makefile["rule"]["build/unkerned-otf/{}.otf".format(GenerateFilename(param))] = {
            "depend": ["build/otd/{}.otz".format(GenerateFilename(param))],
            "command": [
                "mkdir -p build/unkerned-otf/",
                "zstd -d $< --stdout | otfccbuild -q -O3 --keep-average-char-width -o $@",
            ],
        }
        if param["encoding"] == "unspec":
            nowarOtdDeps.add(json.dumps(param))
        else:
            unspec = {**param, "encoding": "unspec"}
            nowarOtdDeps.add(json.dumps(unspec))
            makefile["rule"]["build/otd/{}.otz".format(GenerateFilename(param))] = {
                "depend": ["build/otd/{}.otz".format(GenerateFilename(unspec))],
                "command": ["python set-encoding.py {}".format(ParamToArgument(param))]
            }

    # resolve deps -- nowar otd
    for param in nowarOtdDeps:
        param = json.loads(param)
        dep = ResolveDependency(param)
        makefile["rule"]["build/otd/{}.otz".format(GenerateFilename(param))] = {
            "depend": [
                "build/noto/{}.otz".format(GenerateFilename(dep["Latin"])),
                "build/shs/{}.otz".format(
                    GenerateFilename(dep["CJK"])),
            ] + ([
                "build/noto/{}.otz".format(
                    GenerateFilename(dep["Numeral"]))
            ] if "Numeral" in dep else []) + ([
                "build/roman/{}.otz".format(
                    GenerateFilename(dep['Roman']))
            ] if "Roman" in dep else []),
            "command": [
                "mkdir -p build/otd/",
                "python merge.py {}".format(ParamToArgument(param))
            ]
        }

        makefile["rule"][f"build/noto/{GenerateFilename(dep['Latin'])}.otz"] = {
            "depend": [f"build/noto/{GenerateFilename(dep['Latin'])}.otf"],
            "command": [
                "otfccdump --glyph-name-prefix latn --ignore-hints $< --no-bom | zstd -o $@ --force",
            ]
        }
        notoInstance = [['wght', AxisMapNotoWgth(dep['Latin']['weight'])],
                        ['wdth', AxisMapNotoWdth(dep['Latin']['width'])]]
        makefile["rule"][f"build/noto/{GenerateFilename(dep['Latin'])}.otf"] = {
            "depend": [f"source/noto/NotoSans-VF.otf"],
            "command": [
                "mkdir -p build/noto/",
                f"node --max-old-space-size=2048 instancer.js {ParamToArgument({'input': '$<', 'output': '$@', 'instance': notoInstance})}",
            ]
        }

        if "Numeral" in dep:
            makefile["rule"][f"build/noto/{GenerateFilename(dep['Numeral'])}.otz"] = {
                "depend": [f"build/noto/{GenerateFilename(dep['Numeral'])}.otf"],
                "command": [
                    "otfccdump --glyph-name-prefix latn --ignore-hints $< --no-bom | zstd -o $@ --force",
                ]
            }
            notoInstance = [['wght', AxisMapNotoWgth(dep['Numeral']['weight'])],
                            ['wdth', AxisMapNotoWdth(dep['Numeral']['width'])]]
            makefile["rule"][f"build/noto/{GenerateFilename(dep['Numeral'])}.otf"] = {
                "depend": [f"source/noto/NotoSans-VF.otf"],
                "command": [
                    "mkdir -p build/noto/",
                    f"node --max-old-space-size=2048 instancer.js {ParamToArgument({'input': '$<', 'output': '$@', 'instance': notoInstance})}",
                ]
            }

        if "Roman" in dep:
            makefile["rule"][f"build/roman/{GenerateFilename(dep['Roman'])}.otz"] = {
                "depend": [f"build/noto/{GenerateFilename(dep['Roman'])}.otf"],
                "command": [
                    "mkdir -p build/roman/",
                    "otfccdump --glyph-name-prefix roman --ignore-hints $< --no-bom | zstd -o $@ --force",
                ]
            }
            notoInstance = [['wght', AxisMapNotoWgth(dep['Roman']['weight'])],
                            ['wdth', AxisMapNotoWdth(dep['Roman']['width'])]]
            makefile["rule"][f"build/noto/{GenerateFilename(dep['Roman'])}.otf"] = {
                "depend": [f"source/noto/NotoSans-VF.otf"],
                "command": [
                    "mkdir -p build/noto/",
                    f"node --max-old-space-size=2048 instancer.js {ParamToArgument({'input': '$<', 'output': '$@', 'instance': notoInstance})}",
                ]
            }

        makefile["rule"][f"build/shs/{GenerateFilename(dep['CJK'])}.otz"] = {
            "depend": [f"build/shs/{GenerateFilename(dep['CJK'])}.otf"],
            "command": [
                "otfccdump --glyph-name-prefix hani --ignore-hints $< --no-bom | zstd -o $@ --force",
            ]
        }
        shsInstance = [['wght', AxisMapShsWght(dep['CJK']['weight'])]]
        makefile["rule"][f"build/shs/{GenerateFilename(dep['CJK'])}.otf"] = {
            "depend": [f"source/shs/{dep['CJK']['region']}-VF.otf"],
            "command": [
                "mkdir -p build/shs/",
                f"node --max-old-space-size=2048 instancer.js {ParamToArgument({'input': '$<', 'output': '$@', 'instance': shsInstance})}",
            ]
        }

    # dump `makefile` dict to actual “GNU Makefile”
    makedump = ""

    for var, val in makefile["variable"].items():
        makedump += "{}={}\n".format(var, val)

    for tar, recipe in makefile["rule"].items():
        dep = recipe["depend"] if "depend" in recipe else []
        makedump += "{}: {}\n".format(tar, " ".join(dep))
        com = recipe["command"] if "command" in recipe else []
        for c in com:
            makedump += "\t{}\n".format(c)

    with codecs.open("Makefile", 'w', 'UTF-8') as mf:
        mf.write(makedump)
