from app.post_analysis.domain.post_analysis import PostAnalysisResult


class TestPostAnalysisResult:
    def test_post_analysis_result_init(self):
        """PostAnalysisResult가 title, content, keywords로 생성됨"""
        result = PostAnalysisResult(
            title="삼성전자 실적 발표",
            content="삼성전자가 좋은 실적을 발표했습니다.",
            keywords=["삼성전자", "실적", "반도체"]
        )

        assert result.title == "삼성전자 실적 발표"
        assert result.content == "삼성전자가 좋은 실적을 발표했습니다."
        assert result.keywords == ["삼성전자", "실적", "반도체"]