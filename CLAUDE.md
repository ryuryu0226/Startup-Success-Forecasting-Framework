# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Startup Success Forecasting Framework (SSFF) は、スタートアップの成功可能性を自動評価するシステムです。LLM、機械学習、リアルタイム市場データ分析を統合しています。

論文: https://arxiv.org/abs/2405.19456

## 主要コマンド

### 開発環境の起動

```bash
# Streamlit Web UIの起動
streamlit run app.py

# メインパイプラインの実行
python overallPipeline.py

```

### 品質チェック

```bash
# Pylintでコード品質チェック
pylint $(git ls-files '*.py')
```

## アーキテクチャと構造

### マルチエージェントシステム

- **FounderAgent** (`agents/founder_agent.py`): 創業者の背景とスキルを分析し、L1-L5 のセグメンテーションを実行
- **MarketAgent** (`agents/market_agent.py`): SerpAPI 経由でリアルタイム市場データを取得・分析
- **ProductAgent** (`agents/product_agent.py`): プロダクトの革新性と市場適合性を評価
- **VCScoutAgent** (`agents/vc_scout_agent.py`): VC 視点での総合評価を提供
- **IntegrationAgent** (`agents/integration_agent.py`): 全エージェントの分析を統合し最終評価を生成

### データフロー

1. 創業者情報入力 → FounderAgent でセグメンテーション（L1-L5）
2. 並列処理: MarketAgent（市場分析）、ProductAgent（プロダクト分析）
3. VCScoutAgent で初期評価
4. 機械学習モデルで予測スコア生成
5. IntegrationAgent で全情報を統合し最終レポート作成

## 必須環境設定

### API キー（`.env`ファイル）

```bash
OPENAI_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here
DEFAULT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-ada-002
```

### プロジェクトファイル構造

```
project_root/
├── agents/                  # コアエージェントロジック
│   ├── base_agent.py
│   ├── founder_agent.py
│   ├── integration_agent.py
│   ├── market_agent.py
│   ├── product_agent.py
│   └── vc_scout_agent.py
├── models/                  # 訓練済みモデル
│   ├── neural_network.keras
│   ├── random_forest_classifier.joblib
│   └── trained_encoder_RF.joblib
├── schemas/                 # Pydanticスキーマ定義
│   ├── __init__.py
│   ├── founder_schema.py
│   ├── integration_schema.py
│   ├── market_schema.py
│   ├── product_schema.py
│   └── vc_scout_schema.py
├── utils/                   # ユーティリティスクリプト
│   ├── openai_api.py
│   ├── google_search_api.py
│   └── config.py
├── prompts/                 # プロンプト定義ファイル
│   ├── founder_prompt.py
│   ├── integration_prompt.py
│   ├── market_prompt.py
│   ├── product_prompt.py
│   └── vc_scout_prompt.py
├── app.py                   # StreamlitのWebUI
├── ssff_framework.py        # メインフレームワーク
└── requirements.txt         # 依存パッケージ
```

## 重要な実装詳細

### 創業者セグメンテーション基準

- **L5**: 連続起業家、大企業幹部経験（成功率 92%）
- **L4**: スタートアップ経験者、関連分野の深い専門知識（成功率 74%）
- **L3**: 業界経験者、MBA/高等教育（成功率 56%）
- **L2**: 関連分野の基礎経験（成功率 38%）
- **L1**: 起業・業界経験なし（成功率 24%）

### エラーハンドリング

- API 呼び出しは全て try-except でラップ
- SerpAPI エラー時は代替分析を実行
- データファイル不在時は明確なエラーメッセージ

### パフォーマンス最適化

- エージェント分析は並列実行可能
- 結果はキャッシュ可能（Streamlit の`@st.cache_data`使用）
