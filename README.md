[![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=Python)](https://python.org)

![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-orange)

[![pages-build-deployment](https://github.com/thevickypedia/throne-trader/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/thevickypedia/throne-trader/actions/workflows/pages/pages-build-deployment)

# ThroneTrader

A collection of algorithms to analyze, categorize and predict stocks.

These algorithms are used to assess stocks, and make predictions about future stock prices.

The collection of algorithms leverage data analysis, machine learning, and statistical methods to achieve its objectives in the context of financial markets and investments.

> :bulb: While individual algorithms may lack optimal accuracy, the aggregation of multiple algorithms proves valuable and effective in enhancing overall prediction accuracy.

> :warning: Please note that stock prediction is inherently challenging, and the accuracy of any prediction model will depend on the quality and relevance of the data used, the choice of algorithms, and the changing dynamics of the stock market. Continuous evaluation and improvement of the model are essential to enhance its predictive capabilities.

## Components
- [**Predict stock price using deep learning models**][dl_trade]
- [**Analyze stock price using machine learning models**][ml_trade]
- [**Generate buy/sell/hold signals using real time data**][realtime]
- [**Generate buy/sell/hold signals using financial strategies**][strategies]

## Sample Notebooks
- [**Long Short-Term Memory**][lstm]
- [**Gradient Boosting**][gradient]
- [**Linear Regression**][linear]

## Disclaimer
Remember to thoroughly backtest and paper trade any strategy before using real funds, and always exercise caution and risk management when trading stocks.

<details>
<summary>Why <code>throne-trader</code>?</summary>

<br>

<i>This name draws inspiration from the "Game of Thrones" series, where various characters vie for the Iron Throne, 
symbolizing power, wealth, and influence.
<br><br>
"ThroneTrader" signifies the algorithm's quest for dominance in the financial markets.
<br><br>
It suggests that my trading algorithm is on a mission to conquer the markets and achieve victory, 
much like the characters in the show strive to sit upon the Iron Throne.</i>

</details>

## Linting
`PreCommit` will ensure linting, and the doc creation are run on every commit.

**Requirement**
```shell
pip install sphinx==5.1.1 pre-commit recommonmark pytest
```

**Usage**
```shell
pre-commit run --all-files
```

## Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

[GitHub Pages][docs]

## License & copyright

&copy; Vignesh Rao

Licensed under the [MIT License][license]

[dl_trade]: https://github.com/thevickypedia/throne-trader/blob/main/markdown/DL_ALGORITHMS.md
[ml_trade]: https://github.com/thevickypedia/throne-trader/blob/main/markdown/ML_ALGORITHMS.md
[realtime]: https://github.com/thevickypedia/throne-trader/blob/main/markdown/REALTIME.md
[strategies]: https://github.com/thevickypedia/throne-trader/blob/main/markdown/STRATEGIES.md
[license]: https://github.com/thevickypedia/throne-trader/blob/main/LICENSE
[docs]: https://thevickypedia.github.io/throne-trader/
[lstm]: https://github.com/thevickypedia/throne-trader/blob/main/notebook/lstm.ipynb
[gradient]: https://github.com/thevickypedia/throne-trader/blob/main/notebook/gradient_boosting.ipynb
[linear]: https://github.com/thevickypedia/throne-trader/blob/main/notebook/linear_regression.ipynb
