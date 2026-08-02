# Instrukcja wysłania do Google i YouTube

## Co jest już przygotowane w repozytorium

- publiczna strona opisująca integrację YouTube;
- rozszerzona Polityka Prywatności z Google/YouTube, Limited Use, retencją i linkiem do cofania dostępu;
- uzupełniony Regulamin i instrukcja usuwania danych;
- mechanizm kontroli ważności autoryzacji i usuwania danych YouTube po 30 dniach nieważnego dostępu;
- cofanie tokenu przed rozłączeniem konta i przed trwałym usunięciem organizacji;
- brak zapisu pełnej surowej odpowiedzi API po uploadzie;
- gotowe odpowiedzi do formularzy, uzasadnienia zakresów, macierz danych, checklisty i scenariusz filmu.

## Dane, które musisz uzupełnić sam

1. Pełne imię i nazwisko osoby składającej wniosek.
2. Dokładna nazwa prawna podmiotu prowadzącego ShopAuth Cloud; jeżeli działasz jako osoba fizyczna/JDG, wpisz stan faktyczny.
3. Adres i telefon wymagany przez formularz.
4. Numer projektu Google Cloud skopiowany z panelu projektu.
5. Realna prognoza liczby podłączonych kanałów po 3, 6 i 12 miesiącach.
6. Konto recenzenta BrightBean i osobny testowy kanał YouTube. Hasła nie zapisuj w repozytorium ani PDF.

## Kolejność działań

1. Zleć review i wdrożenie gałęzi `codex/youtube-api-audit-pack`.
2. Po wdrożeniu sprawdź wszystkie pozycje z `evidence_checklist.md`.
3. W Google Search Console potwierdź własność domeny `shopauth.cloud` kontem, które jest Ownerem albo Editorem projektu Google Cloud.
4. W Google Auth Platform ustaw dokładnie dane z `oauth_verification_submission.md`.
5. Ustaw status aplikacji na Production i wyślij osobny wniosek OAuth Verification.
6. Nagraj demo według `reviewer_demo_script.md`. Najbezpieczniej użyć osobnego testowego workspace i kanału; nie rozłączaj `@godfather.a.i` bez osobnej zgody.
7. Wgraj film jako niepubliczny/unlisted na nośnik akceptowany przez formularz i sprawdź link w trybie incognito.
8. Otwórz formularz audytu YouTube: https://support.google.com/youtube/contact/yt_api_form?hl=en
9. Wklej odpowiedzi z `youtube_api_audit_responses.md`, dołącz dossier PDF i link do filmu.
10. Nie zaznaczaj zwiększenia quota, jeżeli nie jest potrzebne. Celem tego wniosku jest audyt zgodności i zniesienie ograniczenia uploadów do Private.
11. Monitoruj adresy właścicieli/edytorów projektu, folder spam oraz odpowiedzi z zespołu Google/YouTube.

## Ważne bramki

- Samo OAuth Verification nie znosi automatycznie ograniczenia `videos.insert` do Private dla niezaudytowanego projektu.
- Sam audyt YouTube nie zastępuje weryfikacji ekranu OAuth i zakresów.
- Publiczne strony muszą być już wdrożone przed nagraniem i wysłaniem.
- Film musi pokazać każdy zakres faktycznie żądany przez produkcyjną aplikację.
- Nie wysyłaj klient secret, tokenów ani haseł w PDF, e-mailu lub nagraniu.
