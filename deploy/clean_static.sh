#!/bin/bash

root='/tmp/static/'


Uglifyjs='/usr/local/Cellar/node/8.0.0_1/bin/uglifyjs'
CleanCss='/usr/local/Cellar/node/8.0.0_1/bin/cleancss'
ComboCss='/usr/local/Cellar/node/8.0.0_1/bin/csscombo'

cd ${root}

echo "*** compress js ***";
cd js/
find . -type f -name '*.js' -exec bash -c "${Uglifyjs} {} > {}.tmp; mv -f {}.tmp {}" \;

cd ${root}

echo "*** compress css ***";
cd css/web
CssList=$(find . -type f -name '*.css' -exec basename {} \;)
for css in ${CssList}
do
    ${ComboCss} ${css} combo.${css}
    ${CleanCss} combo.${css} > ${css}
    rm -f combo.${css}
done
