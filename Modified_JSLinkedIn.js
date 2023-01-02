const puppeteer = require('puppeteer');
const fs = require('fs');
const resolve = require('path').resolve


async function puppeteer_get_info(page) {

    user_info = []
    out_info = {}
    username = await page.$eval('.mt2 h1', el => el.innerText)
    user_info = await page.$eval('.mt2', el => el.innerText)
    out_info['Username'] = username
    out_info['Intro'] = user_info

    temp_out_info = await page.evaluate(() => {
        temp_info = {}
        sections = document.querySelectorAll('section')
        sections.forEach(function (section, i) {
            header = section.querySelector('span')
            if (header) {
                console.log(header)
                if (header.innerText == 'About') {
                    about_text = section.innerText.split('\n')
                    temp_info['About'] = about_text[2]
                }
                if (header.innerText == 'Experience') {
                    experience_info = {}
                    section.querySelectorAll('li.artdeco -list__item').forEach(function (li, i) {
                        experience_name = li.querySelector('span .visually-hidden').innerText
                        experience_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            experience_des.push(div.innerText)
                        })
                        if (experience_info[experience_name]) {
                            experience_name += '-2'
                        }
                        if (experience_info[experience_name]) {
                            experience_name += '-3'
                        }
                        experience_info[experience_name] = experience_des
                    })
                    temp_info['Experience'] = experience_info
                }
                if (header.innerText == 'Education') {
                    education_info = {}
                    section.querySelectorAll('li.artdeco-list__item').forEach(function (li, i) {
                        education_name = li.querySelector('span .visually-hidden').innerText
                        education_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            education_des.push(div.innerText)
                        })
                        if (education_info[education_name]) {
                            education_name += '-2'
                        }
                        if (education_info[education_name]) {
                            education_name += '-3'
                        }
                        education_info[education_name] = education_des
                    })
                    temp_info['Education'] = education_info
                }
                if (header.innerText == 'Courses') {
                    course_info = {}
                    section.querySelectorAll('li.artdeco-list__item').forEach(function (li, i) {
                        course_name = li.querySelector('span .visually-hidden').innerText
                        course_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            course_des.push(div.innerText)
                        })
                        if (course_info[course_name]) {
                            course_name += '-2'
                        }
                        if (course_info[course_name]) {
                            course_name += '-3'
                        }
                        course_info[course_name] = course_des
                    })
                    temp_info['Courses'] = course_info
                }
                if (header.innerText == 'Interests') {
                    interest_info = {}
                    section.querySelectorAll('li.artdeco-list__item').forEach(function (li, i) {
                        interest_name = li.querySelector('span .visually-hidden').innerText
                        interest_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            interest_des.push(div.innerText)
                        })
                        if (interest_info[interest_name]) {
                            interest_name += '-2'
                        }
                        if (interest_info[interest_name]) {
                            interest_name += '-3'
                        }
                        interest_info[interest_name] = interest_des
                    })
                    temp_info['Interests'] = interest_info
                }
                if (header.innerText == 'Skills') {
                    skill_info = {}
                    section.querySelectorAll('li.artdeco-list__item').forEach(function (li, i) {
                        skill_name = li.querySelector('span .visually-hidden').innerText
                        skill_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            skill_des.push(div.innerText)
                        })
                        if (skill_info[skill_name]) {
                            skill_name += '-2'
                        }
                        if (skill_info[skill_name]) {
                            skill_name += '-3'
                        }
                        skill_info[skill_name] = skill_des
                    })
                    temp_info['Skills'] = skill_info
                }
                if (header.innerText == 'Licenses & certifications') {
                    licenses_info = {}
                    section.querySelectorAll('li.artdeco-list__item').forEach(function (li, i) {
                        license_name = li.querySelector('span .visually-hidden').innerText
                        license_des = []
                        li.querySelectorAll('.visually-hidden').forEach(function (div, i) {
                            license_des.push(div.innerText)
                        })
                        if (licenses_info[license_name]) {
                            license_name += '-2'
                        }
                        if (licenses_info[license_name]) {
                            license_name += '-3'
                        }
                        licenses_info[license_name] = license_des
                    })
                    temp_info['licenses'] = licenses_info
                }
            }

        })
        return temp_info
    })


    for (key in temp_out_info) {
        out_info[key] = temp_out_info[key]
    }
    console.log('aa', out_info)
    return out_info
}

puppeteer.launch({
    ignoreDefaultArgs: ["--enable-automation"],
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
}).then(async browser => {

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36")
    const client = await page.target().createCDPSession();
    download_path = resolve('./PDFfiles/Tara_Byrd')
    client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: download_path
    });
    await page.goto('https://www.linkedin.com/login/');

    await page.type('#username', 'sgluegumskno@rambler.ru');
    await page.type('#password', "MFXZRnFFxF9");
    await page.click('.btn__primary--large');

    await page.waitForSelector('a.ember-view')
    await page.click('a.ember-view');

    await page.waitForSelector('#main .artdeco-dropdown__content-inner li:nth-child(3) div')
    await page.$eval('#main .artdeco-dropdown__content-inner li:nth-child(3) div', el => {
        el.click()
    })

    await page.evaluate(async () => {
        await new Promise(function (resolve) {
            setTimeout(resolve, 8000)
        });
    })

    out = {}
    out['1'] = await puppeteer_get_info(page)

    await page.goto('https://www.linkedin.com/in/laurenceaikens/');
    client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: resolve('./PDFfiles/laurenceaikens')
    });
    await page.waitForSelector('#main .artdeco-dropdown__content-inner li:nth-child(3) div')
    await page.$eval('#main .artdeco-dropdown__content-inner li:nth-child(3) div', el => {
        el.click()
    })

    await page.evaluate(async () => {
        await new Promise(function (resolve) {
            setTimeout(resolve, 8000)
        });
    })
    out['2'] = await puppeteer_get_info(page)
    jsonContent = JSON.stringify(out)
    fs.writeFile("output.json", jsonContent, 'utf8', function (err) {
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
        console.log("JSON file has been saved.");
    });
});
