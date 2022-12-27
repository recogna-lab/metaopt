// Configure MathJax
window.MathJax = {
    startup: {
        typeset: false
    },
    tex: {
        inlineMath: [
            ["$", "$"],
            ["\\(", "\\)"]
        ]
    },
    options: {
        menuOptions: {
            settings: {
                zoom: 'Click',
                zscale: '200%'
            }
        }
    },
    chtml: {
        scale: 1.05,
        minScale: 1,
    }
}