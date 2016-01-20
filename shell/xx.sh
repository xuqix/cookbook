#!/bin/bash

cat > ${encoder} <<'EOF'
use URI::Escape;
my $msg = "";
my @lines = <STDIN>;

my $msg = uri_escape("@lines");
print $msg . "n";

exit 0;
EOF

function encode()
{
    echo -n "$@" | perl ${encoder}
}

note=Nagios
smsto=$1
