# Startup Success Forecasting Framework (SSFF)

Startup Success Forecasting Framework (SSFF) は、スタートアップの成功可能性を自動評価するための先駆的なアプローチです。従来の機械学習モデル、大規模言語モデル（LLM）、リアルタイム市場データ分析を組み合わせ、初期段階のスタートアップの実行可能性について深い実用的な洞察を提供することで、ベンチャーキャピタル投資の領域を変革することを目指しています。

論文: https://arxiv.org/abs/2405.19456

## プロジェクト構造

```
project_root/
│
├── agents/                  # Core agent logic (founder, market, product, etc.)
├── models/                  # Trained model artifacts (e.g., .keras, .joblib)
├── utils/                   # Utility scripts, configuration, API wrappers
│
├── app.py                   # Main Streamlit application for web interface
├── ssff_framework.py        # Core SSFF framework logic
│
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
└── README.md                # This file
```

## 環境設定

このプロジェクトの環境を設定するには、以下の手順に従ってください：

1. Python 3.7+ がシステムにインストールされていることを確認してください。

2. リポジトリをクローンします：

   ```
   git clone https://github.com/your-username/Startup-Success-Forecasting-Framework.git
   cd Startup-Success-Forecasting-Framework
   ```

3. 仮想環境を作成します：

   ```
   python -m venv myenv
   ```

4. 仮想環境を有効化します：

   - Windows の場合:
     ```
     myenv\Scripts\activate
     ```
   - macOS と Linux の場合:
     ```
     source myenv/bin/activate
     ```

5. 必要なパッケージをインストールします：

   ```
   pip install -r requirements.txt
   ```

6. プロジェクトルートに `.env` ファイルを作成し、API キーを追加します：

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

7. 完了後に仮想環境を無効化するには：
   ```
   deactivate
   ```

## 実行方法

メインパイプラインを実行してスタートアップを分析するには、Streamlit Web アプリケーションを実行します：

```bash
streamlit run app.py
```

### このフレームワークは 2 つの動作モードをサポートしています：

- **シンプルモード**: 事前定義された基準に基づく迅速な評価を提供
- **アドバンスドモード**: 外部市場データ、創業者レベルのセグメンテーション、ニュアンスに富んだ洞察のためのカスタム LLM プロンプトを組み込んだ詳細分析を提供
