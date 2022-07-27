**English** [简体中文](README-Hans.md) [繁體中文](README-Hant.md)

# Dragonflight Sans (Nowar Sans Slim for _World of Warcraft: Dragonflight_)

This is Nowar Sans, font packs for _World of Warcraft_ and _WoW Classic_ that support all client languages. Nowar Sans is based on [Noto Sans](https://github.com/googlefonts/noto-fonts) and [Source Han Sans](https://github.com/adobe-fonts/source-han-sans).

> Make Love, Not Warcraft.<br>
> 要有爱，不要魔兽争霸。<br>
> 要愛，不要魔獸。

![Nowar Sans](poster/heading.png)

![Multilingual support](poster/multilingual.png)

## Download the Fonts

[Latest release at GitHub](https://github.com/nowar-fonts/Nowar-Sans-Dragonflight/releases)

Nowar Sans is shipped in 7 weights and several regional variants. More weights (any number from 200 to 900!) can be built form source.

### Weights

* 300: Light
* 350: SemiLight
* 400: Regular
* 450: Book
* 500: Medium
* 600: SemiBold
* 700: Bold

![Font weights](poster/weight.png)

### Regional Variants

Bliz and Neut are “standard variants” with regional Chinese character orthographies.

|      | European and 한국어 | 简体中文       | 繁體中文 | Note                                       |
| ---- | ------------------- | -------------- | -------- | ------------------------------------------ |
| Bliz | Mainland China (UI) | Mainland China | Taiwan   | Acts like WoW’s default fallback setting.  |
| Neut | Classical (UI)      | Mainland China | Taiwan   | Prefers classical orthography on fallback. |

CL is the “classical variant” with classical Chinese character orthography (aka Kāngxī Dictionary forms).

|    | European and 한국어 | 中文      |
| -- | ------------------- | --------- |
| CL | Classical (UI)      | Classical |

* European: English, Español (AL), Português, Deutsch, Español (EU), Français, Italiano, and Русский.
* UI: Ambiguous punctations are treated as Western; CJK puctations are half-width.
* Common fonts: `FRIZQT__` and `ARIALN`, which are hard-coded in some addons.

### PTR Cross Language Distributions (XLang)

CyR (Cyrillic Romanisation), Pinyin and Romaja are “cross-language variants” for PTR realms that transliterate or transcript Cyrillic, Chinese and Hanguel characters to Latin letters.

| Variant | Description | Example |
| ------- | ----------- | ------- |
| CyR | *Replace* Cyrillic letters with underlined smapp-capital Latin letters, using the ISO 9:1995 (or GOST 2002) system | R̲ᴜ̲s̲s̲ᴋ̲ɪ̲ᴊ̲ (Русский) |
| Pinyin | *Append* small-capital Hànyǔ Pīnyīn to Chinese characters | 汉ʜᴀ̀ɴ字ᴢɪ̀ |
| Romaja | *Append* small-capital Romaja to Hanguel characters | 한ʜᴀɴ글ɢᴜᴇʟ |

Due to the technical limitation, the CyR is implemented as feature variant and is applied to all languages (we can not distinguish cyrillic chat font from latin chat font – they are both `ARAILN`) while Pinyin and Romaja are implemented as regional variant and are applied to non-Chinese or non-Korean languages (applying to native language will heavily break UI layout).

| Variant | Implementation                   | Applied to                       |
| ------- | -------------------------------- | -------------------------------- |
| CyR     | Feature variant                  | All languages                    |
| Pinyin  | Regional variant (based on Neut) | All except 简体中文 and 繁體中文 |
| Romaja  | Regional variant (based on Neut) | All except 한국어                |

As a result, the XLang variants can be confusing and thus are distributed under a dedicated tag with an `-xlang` suffix.

| Distribution      | CyR | Pinyin | Romaja |
| ----------------- | --- | ------ | ------ |
| Pinyin,Romaja,CyR | ✓   | ✓      | ✓      |
| Pinyin,CyR        | ✓   | ✓      | ✗      |
| Romaja,CyR        | ✓   | ✗      | ✓      |
| Neut,CyR          | ✓   | ✗      | ✗      |
| Pinyin,Romaja     | ✗   | ✓      | ✓      |
| Pinyin            | ✗   | ✓      | ✗      |
| Romaja            | ✗   | ✗      | ✓      |

## How to Build

Almost same as [Nowar Sans](https://github.com/nowar-fonts/Nowar-Sans), except that required Source Han Sans (subset) files are included, and customized regional variants are not supported.

## Credit

Latin, Greek and Cyrillic characters are built from [Noto Source](https://github.com/googlefonts/noto-source), the source “code” for [Noto Sans](https://github.com/googlei18n/noto-fonts) by Google.

CJK Ideographs, Kana and Hangul are from [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) by Adobe.

The traditional Chinese to simplified Chinese conversion table is from [Open Chinese Convert project](https://github.com/BYVoid/OpenCC).
