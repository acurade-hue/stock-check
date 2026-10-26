# Yu Nishimura 판화 재입고 알림

[상품 페이지](https://shop.lafayetteanticipations.com/en/products/impression-edition-limitee-yu-nishimura)를 GitHub 서버가 10분마다 확인합니다. SOLD OUT이 풀리면 폰의 ntfy 앱으로 알림이 옵니다. 알림을 누르면 상품이 담긴 결제 페이지가 바로 열립니다. 결제는 직접 하셔야 합니다.

## 1. 폰에 ntfy 설치 (가입 필요 없음)
1. 앱스토어나 구글플레이에서 **ntfy**를 설치합니다.
2. 앱에서 **+** 를 누르고 채널 이름을 입력해 구독합니다.
   - 추측하기 어렵게 정합니다. 예: `yu-nishimura-k7q2xp9m`
   - 이 이름은 비밀번호처럼 다루고, 다른 사람에게 알려주지 않습니다.
3. 무음 모드에서도 울리게 하려면 앱 설정에서 해당 채널의 "최고 우선순위" 알림 소리를 켭니다.

## 2. GitHub 준비 (보안 설정 먼저)
1. https://github.com 에서 무료로 가입합니다.
2. **2단계 인증 켜기**: Settings → Password and authentication → Two-factor authentication
3. **이메일 비공개**: Settings → Emails → "Keep my email addresses private" 체크

## 3. 저장소 만들고 파일 올리기
1. 오른쪽 위 **+** → **New repository**를 누릅니다.
   - 이름은 자유롭게 정합니다. 예: `stock-check`
   - **Public**을 선택합니다. 공개 저장소는 무료로 무제한 실행되고, 비공개는 무료 한도를 넘습니다.
   - "Add a README file"에 체크하고 **Create repository**를 누릅니다.
2. **Add file → Upload files**에서 `check_stock.py`를 드래그해 올리고 **Commit changes**를 누릅니다.
3. 실행 일정 파일은 폴더 구조가 필요해서 웹에서 직접 만듭니다.
   - **Add file → Create new file**을 누릅니다.
   - 파일 이름 칸에 `.github/workflows/check.yml`을 입력합니다(`/`를 치면 폴더가 만들어집니다).
   - 내 `check.yml` 파일 내용을 그대로 복사해 붙여넣고 **Commit changes**를 누릅니다.

## 4. 채널 이름을 비밀값으로 등록
저장소의 **Settings → Secrets and variables → Actions → New repository secret**에서 다음과 같이 등록합니다.
- Name: `NTFY_TOPIC`
- Secret: 1단계에서 정한 채널 이름

## 5. 테스트
1. 저장소의 **Actions** 탭 → 왼쪽 **Stock check** → **Run workflow**를 누릅니다.
2. "테스트 알림 보내기"에 체크하고 실행합니다.
3. 폰에 "테스트 알림"이 오고, 누르면 결제 페이지가 열리면 성공입니다.

이제 10분마다 자동으로 확인합니다.

## 재입고 후
- 재고가 있는 동안은 10분마다 알림이 계속 옵니다.
- 구매했거나 더 이상 필요 없으면 **Actions → Stock check → 오른쪽 위 ··· → Disable workflow**를 누릅니다.
- 사이트 확인에 실패하면 GitHub이 가입한 이메일로 실패 알림을 보냅니다.

## 알아둘 점
- `check.yml`의 `STOP_AFTER` 날짜(UTC)가 지나면 사이트를 확인하지 않습니다. 기간을 바꾸려면 이 날짜만 고치면 됩니다.
- GitHub의 예약 실행은 몇 분 늦어질 수 있습니다.
- 저장소에 60일 동안 변경이 없으면 GitHub이 예약 실행을 자동으로 멈춥니다. 그 전에 GitHub에서 안내 메일이 오며, Actions 탭에서 다시 켤 수 있습니다.

## 보안 체크
- 알림 링크를 열었으면 **주소가 `shop.lafayetteanticipations.com`인지 확인한 뒤** 결제합니다. 채널 이름이 새면 다른 사람이 가짜 알림을 보낼 수 있기 때문입니다.
- 채널 이름은 코드에 쓰지 말고 Secret에만 둡니다.
- 모르는 사람이 보낸 Pull Request는 머지하지 않습니다.
- 이 프로그램은 결제 정보를 전혀 다루지 않습니다.
