#!/bin/bash

perlfile=".temp.pl"
cat > ${perlfile} <<'EOF'
$l = <STDIN>;
print $l;
exit 0;
EOF

echo -n "efef" | perl ${perlfile} > q2
rm $perlfile
