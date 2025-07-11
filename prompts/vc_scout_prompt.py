PARSE_RECORD_PROMPT = """
以下のスタートアップの説明をStartupInfoスキーマに一致する詳細なJSON構造に変換してください。
説明で提供された情報に基づいて、可能な限り多くのフィールドを含めてください。
フィールドの情報が利用できない場合は、そのフィールドをJSONから省略してください。
プロダクトの詳細、技術スタック、プロダクトのユニークな機能や市場適合性に関する情報に特に注意してください。

スタートアップの説明：
{startup_info}
"""

BASIC_EVALUATION_PROMPT = """
経験豊富なVCスカウトとして、以下の情報に基づいてスタートアップを評価してください：
{startup_info}

市場機会、プロダクトの革新、創業チーム、潜在的リスクを含む包括的な分析を提供してください。
1から10の総合的な可能性スコアで結論してください。
"""

ADVANCED_EVALUATION_PROMPT = """
経験豊富なVCスカウトとして、以下の情報に基づいてスタートアップの詳細な評価を提供してください：
{startup_info}

市場機会、プロダクトの革新、創業チーム、潜在的リスクを含む包括的な分析を提供してください。
1から10の総合的な可能性スコア、投資推奨（投資する/見送る）、
推奨の信頼度（0から1）、決定の簡潔な根拠で結論してください。
"""

CATEGORIZATION_PROMPT = """
スタートアップ評価を専門とするアナリストとして、以下の基準に基づいて与えられたスタートアップを分類してください。
提供されたスタートアップ情報に基づいて、以下の各質問に対してカテゴリー別の回答を提供してください。
各フィールドには指定されたカテゴリー別回答のみを使用してください。他の回答は使用しないでください。

1. 業界成長：[Yes/No/N/A]
2. 市場規模：[Small/Medium/Large/N/A]
3. 開発ペース：[Slower/Same/Faster/N/A]
4. 市場適応性：[Not Adaptable/Somewhat Adaptable/Very Adaptable/N/A]
5. 実行能力：[Poor/Average/Excellent/N/A]
6. 資金調達額：[Below Average/Average/Above Average/N/A]
7. 評価額変化：[Decreased/Remained Stable/Increased/N/A]
8. 投資家の支援：[Unknown/Recognized/Highly Regarded/N/A]
9. レビューと推薦：[Negative/Mixed/Positive/N/A]
10. プロダクト・マーケット・フィット：[Weak/Moderate/Strong/N/A]
11. センチメント分析：[Negative/Neutral/Positive/N/A]
12. 革新性の言及：[Rarely/Sometimes/Often/N/A]
13. 最先端技術：[No/Mentioned/Emphasized/N/A]
14. タイミング：[Too Early/Just Right/Too Late/N/A]

StartupCategorizationスキーマに一致するJSON形式で分析を提供してください。
与えられた情報に基づいてカテゴリーを判定できない場合は、「N/A」を使用してください。
JSON構造の外に説明や追加テキストを含めないでください。

スタートアップ情報：
{startup_info}
"""