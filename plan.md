# Test Plan - HexaCore AI Server

TDD 방식으로 테스트를 작성합니다. 각 테스트는 Red → Green → Refactor 순서로 진행합니다.

## Phase 1: Domain Layer (순수 단위 테스트)

### Data Domain
- [x] `test_data_init_with_required_fields` - Data 객체가 필수 필드(title, content, published_at)로 생성됨
- [x] `test_data_init_with_keywords` - Data 객체가 keywords와 함께 생성됨
- [x] `test_data_init_without_keywords_defaults_to_empty_list` - keywords 없이 생성 시 빈 리스트
- [x] `test_data_add_keyword` - add_keyword 메서드가 키워드를 추가함
- [x] `test_data_id_defaults_to_none` - id 기본값이 None

### Keyword Domain
- [x] `test_keyword_init` - Keyword 객체가 name으로 생성됨
- [x] `test_keyword_id_defaults_to_none` - Keyword id 기본값이 None
- [x] `test_keyword_mention_init` - KeywordMention이 keyword_id, name, mention_count로 생성됨

### PostAnalysisResult Domain
- [x] `test_post_analysis_result_init` - PostAnalysisResult가 title, content, keywords로 생성됨

## Phase 2: Use Case Layer (Mock을 사용한 단위 테스트)

### CreateDataList Use Case
- [x] `test_create_data_list_with_single_item` - 단일 항목 생성
- [x] `test_create_data_list_with_multiple_items` - 복수 항목 생성
- [x] `test_create_data_list_strips_keyword_whitespace` - 키워드 공백 제거
- [x] `test_create_data_list_filters_empty_keywords` - 빈 키워드 필터링
- [x] `test_create_data_list_handles_missing_published_at` - published_at 없을 때 빈 문자열 처리

### GetDataList Use Case
- [x] `test_get_data_list_returns_recent_data` - 최근 데이터 반환
- [x] `test_get_data_list_respects_limit` - limit 파라미터 적용

### GetTopKeywords Use Case
- [x] `test_get_top_keywords_returns_mentions` - 상위 키워드 반환
- [x] `test_get_top_keywords_respects_limit` - limit 파라미터 적용

## Phase 3: Repository Port (Interface Contract 테스트)

### DataRepositoryPort
- [x] `test_data_repository_port_has_save_method` - save 메서드 존재
- [x] `test_data_repository_port_has_get_recent_method` - get_recent 메서드 존재

### KeywordRepositoryPort
- [x] `test_keyword_repository_port_has_get_top_mentions_method` - get_top_mentions 메서드 존재

## Phase 4: Integration Tests (선택적)

### API Endpoints
- [x] `test_health_endpoint_returns_ok` - /health 엔드포인트 정상 응답
- [x] `test_get_data_endpoint` - GET /data 엔드포인트
- [x] `test_get_keywords_endpoint` - GET /keywords 엔드포인트

---

## 진행 방법

1. `/go` 명령으로 다음 미완료 테스트를 찾아 구현
2. Red: 실패하는 테스트 작성
3. Green: 테스트 통과하는 최소 코드 작성
4. Refactor: 코드 정리 (구조 변경은 별도 커밋)
5. 완료된 테스트는 `[x]`로 표시