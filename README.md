# WebサイトのURL

https://www.gavo.t.u-tokyo.ac.jp/~miyamoto/webapp/index.cgi/average_face

# Webサイトの概要

学部4年生の時に「音声エージェントの印象に合致する音声の加工強度の予測」というテーマで研究していました。

研究の背景としては、ロボットのような実体を伴う音声エージェントが人間と対話する際、その見た目の印象に合う音声を選択することがエージェントの親しみやすさの点で重要です。ロボットの見た目の印象と音声の印象に乖離がある場合、聞いた人が恐怖感を覚える「不気味の谷」という現象が起こってしまうため、音声エージェントに適した音声をデザインすることが重要です。

音声エージェントに適した音声デザインを実現するために、エージェントの画像に対して適切だと感じる音声を選んでもらう主観的な評価実験を、クラウドソーシングサービスを用いて多数の被験者に対して行い、データを収集しました。その際に作成したWebサイトがこちらになります。

具体的には、音声エージェントの画像を提示し、その印象に合致するように音声を加工してもらい、そのパラメータを収集しました。

# Webサイトのイメージ

<img width="952" alt="guide_image" src="https://github.com/LEEANHUA/webapp/assets/92500020/bcbca6b2-daff-4129-8d05-42e453219eea">

1. 音声エージェントの画像([Stable Diffusion](https://ja.stability.ai/stable-diffusion)を用いて生成したもの)
2. 加工した音声を試聴するボタン
3. 加工のパラメータをデフォルトの値に戻すボタン
4. 音声の加工を終了し、次の問に進むボタン
5. Robopitchという加工法を用いて、音声を機械的に加工することができる
6. Robopitchのパラメータを変更できる
7. 音声の高さ(基本周波数)を上下させることができる
8. 音声をどれだけ高くするか・低くするかを調整できる

# 使用技術一覧

<img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
<img src="https://img.shields.io/badge/Javascript-276DC3.svg?logo=javascript&style=flat">
<img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
<img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
<img src="https://img.shields.io/badge/-Flask-000000.svg?logo=flask&style=flat">
<img src="https://img.shields.io/badge/-SQLite-003B57.svg?logo=sqlite&style=flat">
