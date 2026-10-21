"""Exercise the shipped progress-preserving hotfix page and its recovery guards."""
import hashlib,json,struct,tempfile,zipfile
from pathlib import Path
from verify_sources import checksum
ROOT=Path(__file__).resolve().parents[1]


def main():
    from playwright.sync_api import sync_playwright
    checks=[];rom=(ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    current=(ROOT/'saves/test/P002-office-fixture.sav').read_bytes()
    before=hashlib.sha256(current).hexdigest()
    with tempfile.TemporaryDirectory(prefix='lc-p002a-browser-')as directory:
        temp=Path(directory)
        with zipfile.ZipFile(ROOT/'patches/P002a/P002a-safety-fix.zip')as z:z.extractall(temp)
        html_sha=hashlib.sha256((temp/'Make-Safety-Fix.html').read_bytes()).hexdigest()
        with sync_playwright()as runtime:
            browser=runtime.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
            page=browser.new_page(accept_downloads=True);requests=[]
            page.on('request',lambda request:requests.append(request.url)if request.url.startswith(('http:','https:'))else None)
            url='https://p002a-safety.test/';page.route(url,lambda route:route.fulfill(body=(temp/'Make-Safety-Fix.html').read_text(),content_type='text/html'));page.goto(url)
            assert page.locator('#build').is_disabled();checks.append('requires both ROM and current save')
            page.locator('#save').set_input_files({'name':'current.sav','mimeType':'application/octet-stream','buffer':current})
            for size,data in [(16,rom),(32,rom+b'\xa5'*len(rom))]:
                page.locator('#rom').set_input_files({'name':'current.gba','mimeType':'application/octet-stream','buffer':data})
                page.locator('#build').click();page.wait_for_function("!document.getElementById('download').hidden")
                with page.expect_download()as event:page.locator('#download').click()
                out=temp/'out.gba';event.value.save_as(out);result=out.read_bytes()
                expected=bytearray(data);expected[0xC30C2C:0xC30C2E]=bytes.fromhex('5d3e');expected[0xC80000:0xCA0000]=current
                assert result==bytes(expected)
                checks.append(f'{size}MiB output changes only collision word and embeds supplied current save; upper bytes preserved')
            with page.expect_download()as event:page.locator('#save-download').click()
            out=temp/'out.sav';event.value.save_as(out);assert out.read_bytes()==current;checks.append('exported winning save is byte exact')
            invalid=bytearray(current);invalid[0]^=1
            page.locator('#save').set_input_files({'name':'invalid.sav','mimeType':'application/octet-stream','buffer':bytes(invalid)})
            page.locator('#build').click();page.wait_for_function("document.getElementById('status').textContent.includes('checksum mismatch')")
            assert page.locator('#download').is_hidden();checks.append('invalid save rejected without output')
            stadium=bytearray(current)
            for sector in range(28):
                start=4096*sector
                if struct.unpack_from('<H',stadium,start+0xFF4)[0]==1:
                    stadium[start+4:start+6]=bytes(2)
                    struct.pack_into('<H',stadium,start+0xFF6,checksum(stadium[start:start+0xFF0]))
            page.locator('#save').set_input_files({'name':'stadium.sav','mimeType':'application/octet-stream','buffer':bytes(stadium)})
            page.locator('#build').click();page.wait_for_function("document.getElementById('status').textContent.includes('inside the broken stadium')")
            assert page.locator('#download').is_hidden();checks.append('valid save inside stadium held for recovery, no silent teleport/reset')
            wrong=bytearray(rom);wrong[0xC7213C]^=1
            page.locator('#rom').set_input_files({'name':'wrong.gba','mimeType':'application/octet-stream','buffer':bytes(wrong)})
            page.locator('#save').set_input_files({'name':'current.sav','mimeType':'application/octet-stream','buffer':current})
            page.locator('#build').click();page.wait_for_function("document.getElementById('status').textContent.includes('Game/driver bytes do not match')")
            assert page.locator('#download').is_hidden();checks.append('unrecognized game/driver rejected')
            assert requests==[url];checks.append('no application network requests')
            browser.close()
    assert hashlib.sha256((ROOT/'saves/test/P002-office-fixture.sav').read_bytes()).hexdigest()==before
    checks.append('source winning save unchanged')
    report={'complete':True,'checks_passed':checks,'html_sha256':html_sha,'browser':'Chromium through intercepted secure document; cloud policy blocks file URLs','physical_hardware_tested':False}
    (ROOT/'extracted/builds/P002a-browser-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
