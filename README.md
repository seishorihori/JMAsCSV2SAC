JMAsCSV2SAC
====
This file is written in Japanese (UTF-8 code). 

## Overview
気象庁（JMA）で配布されている震度計データ（CSV形式のファイル）をSAC形式のファイルに変換するためのPythonスクリプト。

## Description
JMAから配布されている震度計データのCSVファイルは、ヘッダー部分のフォーマットが違う2とおりのファイルがあるため、それに対応して、2つのPythonスクリプトを作成した。
* JMA_LGsmCSV2SAC.py：地方自治体で設置した震度計による記録を変換するためのPythonコード。
* JMA_LPsmCSV2.py：長周期地震動に関する情報を公開するサイトで試験的に公開されている
震度計データを変換するためのPythonコード

Python 3.6で作成と動作確認を行い、SAC形式に変換するところはObsPyを使用。

## Demo
なし

## VS. 
同じ目的のコードはいくらでもあると思いますが、比較したことはありません。
Several researchers (mainly seismologists) will create codes for the same purpose, but I have not compared my codes with others.  

## Requirement
* Python 3系列
* NumPy (http://www.numpy.org/)
* ObsPy (https://github.com/obspy/obspy/wiki)
* 他にPythonの標準的と思われるライブラリ：コードの頭に出てくるimport欄を参照のこと。

## Usage
JMA_LGsmCSV2SAC.py、JMA_LPsmCSV2SAC.py共通。

0. 各スクリプトで変換したいCSVファイルが1ヶ所にまとまっていることが前提
1. 変換したいCSVファイルが格納されているディレクトリを、DIR00という変数に書き込む。
2. コードを実行。

※JMA_LPsmCSV2SAC.pyでは、変換したいCSVファイル名の頭5文字が「観測点コード」（気象庁で刊行されている『強震観測報告』DVDによると、正確には震度計番号）であることを仮定している。2018年9月5日現在ではこの仮定は間違ってはいないが、今後、ファイル名の付け方が変わってしまった場合には要検討。ファイルのヘッダー部分にそういう情報が書き込まれていないのが最大の問題と思う……。

# Install
スクリプト自体をダウンロードするだけのはず。Requirementの項に書かれているライブラリーがない場合には別途インストール。

## Contribution
バグリポート、フィードバックは歓迎します。

## Licence
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

※ObsPyのライセンスに従っている。

## Author
堀川晴央 (Horikawa, Haruo)

[seishorihori](https://github.com/seishorihori)
