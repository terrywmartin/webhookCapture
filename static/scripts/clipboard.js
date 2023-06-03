
const copyBtn = [...document.getElementsByClassName('copy-btn')];




copyBtn.forEach(btn => btn.addEventListener('click', () => {
    const copyData = btn.getAttribute('data-copy-text') 
    console.log(copyData)
    let copiedText = ""
    
    //console.log(copyData);
    let copyTxt;
    if (copyData == "URL") {
        copyTxt = document.getElementsByName("endpoint");
        copyTxt[0].select();
        copyTxt[0].setSelectionRange(0, 99999);
        
    }
    else {
        copyTxt = document.getElementsByName("token");
        copyTxt[0].select();
        copyTxt[0].setSelectionRange(0, 99999);
    }
    console.log(copyTxt[0].value)
    
    navigator.clipboard.writeText(copyTxt[0].value)
    navigator.clipboard.readText().then(() => {
        btn.textContent = 'Copied'
        setTimeout((btn) => {btn.textContent = 'Copy to clipboard'}, 3000, btn)

    }).catch(() => {
        alert("Error copying secret to the clipboard")
    })
    
}))


