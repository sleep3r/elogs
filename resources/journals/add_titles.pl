#!/usr/bin/perl
use strict;
use warnings;
binmode STDOUT, ":utf8";
use utf8;
use lib qw(..);
use JSON qw( );
use File::Find::Rule;
use Cwd;

# ======= subroutines ========
sub addTitlesToJournal {
  my $fileName = $_[0];
  print("file path: ".$fileName."\n");

  my $json_text = do {
     open(my $json_file, "<:encoding(UTF-8)", $fileName)
        or die("Can't open \$filename\": $!\n");
     local $/;
     <$json_file>
  };

  my $json = JSON->new(utf8 => 1, pretty => 1);
  my $data = $json->decode($json_text);

  for ( @{$data->{tables}} ) {
       my $item = $_;
       print "table '".$item->{name}."'\n";

       for( @{$item->{fields}}) {
         $_->{title} = $_->{name};
         print "\tfield '".$_->{name}."'\n";
       }

  }

  my $jsn = JSON->new->utf8->pretty(1);
  open my $fh, ">", $fileName;
  print $fh $jsn->encode($data);
  close $fh;

}

sub getAllJournalNames {
  my $cwd = getcwd();
  my @files = File::Find::Rule->file()
                            ->name( '*.json', '*.jrn' )
                            ->in( $cwd );
  return @files;
}

# ======= code ========
my @journalName = getAllJournalNames();
foreach (@journalName) {
   addTitlesToJournal($_);
}
