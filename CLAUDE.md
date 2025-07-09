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

# 実験の実行
python experiments/experiment.py
```

### 品質チェック
```bash
# Pylintでコード品質チェック
pylint $(git ls-files '*.py')
```

## アーキテクチャと構造

### マルチエージェントシステム
- **FounderAgent** (`agents/founder_agent.py`): 創業者の背景とスキルを分析し、L1-L5のセグメンテーションを実行
- **MarketAgent** (`agents/market_agent.py`): SerpAPI経由でリアルタイム市場データを取得・分析
- **ProductAgent** (`agents/product_agent.py`): プロダクトの革新性と市場適合性を評価
- **VCScoutAgent** (`agents/vc_scout_agent.py`): VC視点での総合評価を提供
- **IntegrationAgent** (`agents/integration_agent.py`): 全エージェントの分析を統合し最終評価を生成

### 機械学習パイプライン
- **ニューラルネットワーク** (`algorithms/neuralNetworks.py`): 深層学習による成功予測
- **ランダムフォレスト** (`algorithms/randomForest.py`): アンサンブル学習による予測
- **LLMセグメンテーション** (`algorithms/LLM_Segmentation.py`): GPTを使用した創業者の5段階分類

### データフロー
1. 創業者情報入力 → FounderAgentでセグメンテーション（L1-L5）
2. 並列処理: MarketAgent（市場分析）、ProductAgent（プロダクト分析）
3. VCScoutAgentで初期評価
4. 機械学習モデルで予測スコア生成
5. IntegrationAgentで全情報を統合し最終レポート作成

## 必須環境設定

### APIキー（`.env`ファイル）
```bash
OPENAI_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here
DEFAULT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-ada-002
```

### データファイル構造
```
data/
├── Successful/           # 成功企業のプロファイル
├── Unsuccessful/         # 失敗企業のプロファイル
├── successful/           # セグメント済み成功データ
└── unsuccessful/         # セグメント済み失敗データ
```

## 重要な実装詳細

### 創業者セグメンテーション基準
- **L5**: 連続起業家、大企業幹部経験（成功率92%）
- **L4**: スタートアップ経験者、関連分野の深い専門知識（成功率74%）
- **L3**: 業界経験者、MBA/高等教育（成功率56%）
- **L2**: 関連分野の基礎経験（成功率38%）
- **L1**: 起業・業界経験なし（成功率24%）

### エラーハンドリング
- API呼び出しは全てtry-exceptでラップ
- SerpAPIエラー時は代替分析を実行
- データファイル不在時は明確なエラーメッセージ

### パフォーマンス最適化
- エージェント分析は並列実行可能
- 結果はキャッシュ可能（Streamlitの`@st.cache_data`使用）
- バッチ処理対応（`experiments/experiment.py`）