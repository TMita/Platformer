# I wanna make a game
【概要】  
トラップを避けてゴールを目指すプラットフォームゲームです。  
PythonのPygameライブラリをインストールした環境でプレイができます。   
ゲームを開始するとまず、難易度選択画面に移ります。難易度はイージー、ノーマル、ハードがあり、自分に合った難易度でプレイすることが可能です。  
ステージをクリアするとゲームオーバーになった回数とクリアタイムが記録されます。    

【制作人数・期間】  
1人で1ヶ月ほどかけて制作しました。    

【操作方法】  
左方向キー：左移動  
右方向キー：右移動  
スペース：ジャンプ（２段ジャンプまで可能となっており、ボタンを離すタイミングによって高さを調整できます）  
Rキー：ゲーム開始・再開  
エスケープキー：スタート画面へ戻る    

【ギミック】  
セーブブロック：触れるとその位置から再度プレイすることが可能です。  
水域：キャラクターが水域に侵入すると水中状態になります。水中では浮力が働き、キャラクターの落下する速度が低下します。また、ジャンプできる限界の高さが減少しますが無限ジャンプが可能になります。  
トラップ（針とさくらんぼ）：トラップには移動するものもあり、触れるとゲームオーバーになってしまいます。
