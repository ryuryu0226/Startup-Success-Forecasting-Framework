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

### 機械学習パイプライン

- **ニューラルネットワーク** (`algorithms/neuralNetworks.py`): 深層学習による成功予測
- **ランダムフォレスト** (`algorithms/randomForest.py`): アンサンブル学習による予測
- **LLM セグメンテーション** (`algorithms/LLM_Segmentation.py`): GPT を使用した創業者の 5 段階分類

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
├── algorithms/              # 機械学習アルゴリズム
│   ├── LLM_Segmentation.py
│   ├── neuralNetworks.py
│   ├── randomForest.py
│   └── SerpAPI_Testing.py
├── models/                  # 訓練済みモデル
│   ├── neural_network.keras
│   ├── random_forest_classifier.joblib
│   └── trained_encoder_RF.joblib
├── utils/                   # ユーティリティスクリプト
│   ├── api_wrapper.py
│   └── config.py
├── app.py                   # StreamlitのWebUI
├── ssff_framework.py        # メインフレームワーク
├── overallPipeline.py       # パイプライン実行スクリプト
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

## 重要なファイル

### コア実行ファイル

- `app.py`: Streamlit WebUI のメインファイル
- `ssff_framework.py`: フレームワークの中核実装
- `overallPipeline.py`: パイプライン統合実行
- `baseline_framework.py`: ベースラインモデル実装

### エージェント実装

- `agents/base_agent.py`: 全エージェントの基底クラス
- `agents/founder_agent.py`: 創業者分析エージェント
- `agents/market_agent.py`: 市場分析エージェント
- `agents/product_agent.py`: プロダクト分析エージェント
- `agents/vc_scout_agent.py`: VC 評価エージェント
- `agents/integration_agent.py`: 統合分析エージェント

### 機械学習モデル

- `algorithms/neuralNetworks.py`: ニューラルネットワーク実装
- `algorithms/randomForest.py`: ランダムフォレスト実装
- `algorithms/LLM_Segmentation.py`: LLM ベースのセグメンテーション

### 訓練済みモデル

- `models/neural_network.keras`: 訓練済みニューラルネットワーク
- `models/random_forest_classifier.joblib`: 訓練済みランダムフォレスト
- `models/trained_encoder_RF.joblib`: 特徴量エンコーダー
