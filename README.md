# TextSegmentaion

## 依存関係
* Python 3.4.3
* mecab of 0.994

## 引数(arg)

##### This script is to segment text using LCseg.

``` usage
textseg.py [-h] [-i INPUT_FILE_PATH] [-d DIC] [-g GAP] [-w WINDOW] [-pl P_LIMIT] [-a ALPHA]
```


optional arguments:

|name|arg|description|range|
|:--:|:--:|:--:|:--:|
| HELP |-h, --help | show this help message and exit | |
| INPUT_FILE_PATH | -i, --input_file_path | File path of input text you want to segment. | |
| DIC |-d, --dic | Dictionary path for MeCab | |
| GAP |-g, --gap | 連鎖を分割する空白の長さ | [1,length] |
| WINDOW |-w, --window  | 分析窓幅 | [1,length] |
| P_LIMIT |-pl , --p_limit | 境界線信頼値の足きり閾値 | [-1, 1] |
| ALPHA |-a, --alpha | 仮定した境界線に対する閾値の限界 | [0, 1] |

#### example:
* MeCabの辞書[mecab-ipadic-neologd]を指定して，入力ファイル[./hoge.txt]を分割
```
py textseg.py -i hoge.dat -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/
```