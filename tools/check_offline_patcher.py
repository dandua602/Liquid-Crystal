"""Exercise the shipped offline page in a real browser, including its download.

Optional Playwright plus installed Chromium; no server or network is needed.
"""
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    from playwright.sync_api import sync_playwright
    checks = []
    with tempfile.TemporaryDirectory(prefix='lc-offline-browser-') as directory:
        temp = Path(directory)
        with zipfile.ZipFile(ROOT/'patches/P002/P002-easy-cartridge-test.zip') as archive:
            archive.extractall(temp)
        manifest = json.loads((temp/'MANIFEST.json').read_text())
        source = ROOT/'roms/POKEMON Liquid Crystal.gba'
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                              args=['--no-sandbox', '--disable-dev-shm-usage'])
            page = browser.new_page(accept_downloads=True)
            network = []; errors = []
            page.on('request', lambda request: network.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
            page.on('pageerror', lambda error: errors.append(str(error)))
            # This cloud browser's managed policy blocks file:// navigation.
            # Serve only the initial document through an intercepted secure
            # test URL, with no HTTP server or outbound connection.
            test_url = 'https://cartridge-patcher.test/'
            page.route(test_url, lambda route: route.fulfill(
                body=(temp/'Make-Test-ROM.html').read_text(), content_type='text/html'))
            page.goto(test_url)
            assert page.locator('#create').is_disabled()
            checks.append('button disabled until a ROM is selected')
            page.locator('#rom').set_input_files({'name': 'wrong.gba', 'mimeType': 'application/octet-stream', 'buffer': b'wrong'})
            page.locator('#create').click()
            page.wait_for_function("document.getElementById('status').textContent.includes('wrong size')")
            checks.append('wrong-size input rejected with readable guidance')
            page.locator('#rom').set_input_files(str(ROOT/'roms/1636 - Pokemon Fire Red (U)(Squirrels).gba'))
            page.locator('#create').click()
            page.wait_for_function("document.getElementById('status').textContent.includes('ROM version does not match')")
            checks.append('same-size FireRed ROM rejected by exact source hash')
            assert page.locator('#diagnostics').is_visible()
            assert 'SHA256:' in page.locator('#file-details').text_content()
            checks.append('rejected file shows its actual size and SHA256 for troubleshooting')

            def download_and_check(label, click='#create'):
                with page.expect_download(timeout=60000) as event:
                    page.locator(click).click()
                download = event.value
                assert download.suggested_filename == 'P002-warehouse-test.gba'
                output = temp/'browser-output.gba'; download.save_as(output)
                assert hashlib.sha256(output.read_bytes()).hexdigest() == manifest['targetSha256']
                assert output.read_bytes() == (ROOT/'builds/cartridge/P002-warehouse-test.gba').read_bytes()
                checks.append(label)

            page.locator('#rom').set_input_files(str(source))
            download_and_check('original ROM creates the exact previously tested warehouse ROM')
            assert page.locator('#download').is_visible()
            download_and_check('persistent download link creates the same ROM when clicked again', '#download')
            for version in ('P001', 'P002'):
                page.locator('#rom').set_input_files(str(ROOT/f'builds/dev/Liquid Crystal {version}.gba'))
                download_and_check(f'exact {version} input creates the same tested target')

            changed = bytearray(source.read_bytes()); changed[0xC80000] ^= 1
            newer = temp/'newer-cart-dump.gba'; newer.write_bytes(changed)
            page.locator('#rom').set_input_files(str(newer)); page.locator('#create').click()
            page.wait_for_function("document.getElementById('status').textContent.includes('built-in save has changed')")
            assert page.locator('#download').is_hidden()
            checks.append('compatible changed-save dump requests the original backup without producing unverified output')
            save = ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'
            save_before = hashlib.sha256(save.read_bytes()).hexdigest()
            bad_save = bytearray(save.read_bytes()); bad_save[0] ^= 1
            page.locator('#save').set_input_files({'name': 'wrong.sav', 'mimeType': 'application/octet-stream', 'buffer': bytes(bad_save)})
            page.locator('#create').click()
            page.wait_for_function("document.getElementById('status').textContent.includes('not the original five-badge')")
            checks.append('same-size wrong save rejected by payload hash')
            page.locator('#save').set_input_files(str(save))
            download_and_check('changed-save dump plus original FlashGBX-footer backup produces exact tested target')
            assert hashlib.sha256(save.read_bytes()).hexdigest() == save_before
            assert newer.read_bytes() == bytes(changed)
            checks.append('save backup and changed cart dump remain unchanged')
            changed[0xB9EF00] ^= 1
            damaged = temp/'changed-code.gba'; damaged.write_bytes(changed)
            page.locator('#rom').set_input_files(str(damaged)); page.locator('#create').click()
            page.wait_for_function("document.getElementById('status').textContent.includes('ROM version does not match')")
            assert page.locator('#download').is_hidden()
            checks.append('altered game code rejected even when the correct save backup is selected')
            page.locator('#rom').set_input_files(str(ROOT/'builds/cartridge/P002-warehouse-test.gba'))
            download_and_check('already-correct warehouse test image can be downloaded directly')
            assert network == [test_url], network
            assert not errors, errors
            checks.append('no application HTTP/HTTPS requests after the intercepted initial document, or script errors')
            browser.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before
        checks.append('original input unchanged')
    result = {'complete': True, 'browser': 'Chromium, intercepted secure document; no server or outbound connection',
              'checks_passed': checks, 'target_sha256': manifest['targetSha256'], 'hardware_verified': False,
              'limits': 'Managed cloud browser blocks file URLs. Browser behavior was checked with the same shipped HTML served by a Playwright route; local-file navigation on the user computer is not independently verified here.'}
    (ROOT/'extracted/builds/P002-offline-browser-validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
