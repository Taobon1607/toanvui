const fs = require('fs');
const path = 'd:/toanvui-main/toanvui-main/src/data/problems.js';

try {
    let content = fs.readFileSync(path, 'utf8');
    const prefix = 'export const problems = ';
    
    if (!content.startsWith(prefix)) {
        console.log("Error: File doesn't start with 'export const problems = '");
        process.exit(1);
    }

    let jsonStr = content.substring(prefix.length).trim();
    if (jsonStr.endsWith(';')) {
        jsonStr = jsonStr.slice(0, -1);
    }
    
    let problems = JSON.parse(jsonStr);
    let changed = false;

    for (let id in problems) {
        let p = problems[id];
        if (p.topicId && p.topicId.startsWith('g7-math')) {
            // 1. Remove ABCD prefix
            if (p.question && p.question.includes('ABCD A B C D\n')) {
                p.question = p.question.replace(/ABCD A B C D\n/g, '');
                changed = true;
            }
            
            // 2. Remove leaked section headers
            if (p.choices && p.choices.length > 0) {
                const leakedHeaders = ['ĐẠI SỐ', 'HÌNH HỌC'];
                const originalLength = p.choices.length;
                p.choices = p.choices.filter(c => !leakedHeaders.includes(c));
                if (p.choices.length !== originalLength) {
                    changed = true;
                }
            }
            
            // 3. Degree symbols correction
            const degreeValues = ['300', '450', '600', '900', '1000', '1200', '1800', '500'];
            if (p.choices && p.choices.length > 0) {
                for (let i = 0; i < p.choices.length; i++) {
                    let c = p.choices[i];
                    if (degreeValues.includes(c)) {
                        p.choices[i] = c.slice(0, -1) + '°';
                        changed = true;
                    }
                }
            }
            
            let degreeRegex = /\b(300|450|600|900|1000|1200|1800|500)\b/g;
            if (p.question && degreeRegex.test(p.question)) {
                 p.question = p.question.replace(degreeRegex, (match) => {
                     return match.slice(0, -1) + '°';
                 });
                 changed = true;
            }
            
            // 4. Symbol replacement
            const replaceSymbols = (str) => {
                if (!str) return str;
                return str
                    .replace(//g, '∠')
                    .replace(//g, '△')
                    .replace(//g, '=')
                    .replace(//g, '<')
                    .replace(//g, '>')
                    .replace(//g, '+')
                    .replace(//g, '-')
                    .replace(//g, '*')
                    .replace(//g, '/')
                    .replace(//g, '(')
                    .replace(//g, ')')
                    .replace(//g, "'");
            };

            if (p.question) {
                let oldQ = p.question;
                p.question = replaceSymbols(p.question);
                if (oldQ !== p.question) changed = true;
            }
            
            if (p.choices) {
                 for (let i = 0; i < p.choices.length; i++) {
                     let oldC = p.choices[i];
                     p.choices[i] = replaceSymbols(oldC);
                     if (oldC !== p.choices[i]) changed = true;
                 }
            }
        }
    }
    
    if (changed) {
        fs.writeFileSync(path, prefix + JSON.stringify(problems, null, 2) + ';\n', 'utf8');
        console.log("Successfully fixed problems.js");
    } else {
        console.log("No changes made to problems.js.");
    }

} catch (error) {
    console.error("An error occurred:", error);
}
