#!/usr/bin/perl -w
use strict;

my %d = ();

#foreach my $type ('train', 'dev', 'test') {
#  %{$d{$type}} = ();
# open F, "original/wiki1.$type.qa" or die;
foreach my $type ('train', 'dev', 'test') {
  %{$d{$type}} = ();
  open F, "original/wiki2.$type.qa" or die;
  while (<F>) {
    chomp;
    if (/^\s*$/) { next; }
    die if not /^WIKI/;
    my ($sent_id, $pred_count) = split;
    my $sent = <F>; chomp $sent;
    #print "sent=$sent\n";
    my @sent = split /\s+/, $sent;
    for (my $pred_id=0; $pred_id<$pred_count; $pred_id++) {
      #print STDERR "pred_id=$pred_id/$pred_count\n";
      $_ = <F>; chomp;
      my ($id, $verb, $q_count) = split /\t/, $_;
      #print STDERR "  id=$id verb=$verb\n";
      die if not (lc($verb) eq lc($sent[$id]));
      for (my $q_id=0; $q_id<$q_count; $q_id++) {
        #print STDERR "  q_id=$q_id/$q_count\n";
        $_ = <F>; chomp;
        my @q = split /\t/, $_;
        my @q0 = split /\t/, $_;
        #print STDERR "    q=$_\n";

        my $full_id = "$sent_id.$pred_id.$q_id";
        my $prefix = '';
        my $suffix = '';

        for (my $i=0; $i<@sent; $i++) {
          if ($i < $id) { $prefix .= $sent[$i] . ' '; }
          if ($i > $id) { $suffix .= $sent[$i] . ' '; }
        }
        $prefix =~ s/ $//;
        $suffix =~ s/ $//;

        my $predicate = uc($verb);
        my $answer = $q0[8];

        $q[1] = '*AUX*';
        $q[2] = '*SUBJ*' if $q[2] ne '_';
        $q[3] = '*PRED*' if $q[3] ne '_';
        $q[4] = '*TRG*'  if $q[4] ne '_';
        $q[5] = '*PP*'   if $q[5] ne '_';
        $q[6] = '*OBJ2*' if $q[6] ne '_';
        $q[8] = '*ANS*'  if $q[8] ne '_';
        my $key = join ' ', @q;

        pop @q0;
        my $question = join "\t", @q0;
        $question =~ s/ /~/g;
        $question =~ s/\t/ /g;

        my $me = "$full_id\t$prefix\t$predicate\t$suffix\t$question\t$answer\n";

        if (not defined $d{$type}{$key}) { @{$d{$type}{$key}} = (); }
        push @{$d{$type}{$key}}, $me;
      }
    }
    $_ = <F>;
    chomp;
    die if not ($_ eq '');
  }
  close F;
}


#foreach my $type ('train', 'dev', 'test') {
#  open O, "> tsv/wiki1.$type.tsv" or die;
foreach my $type ('train', 'dev', 'test') {
  open O, "> tsv/wiki2.$type.tsv" or die;

  print O "#id\tprefix\tpredicate\tsuffix\tquestion\tanswer\n";

  my @d = ();
  foreach my $key (keys %{$d{$type}}) {
    next if (not defined $d{'train'}{$key});
    next if (scalar @{$d{'train'}{$key}} < 100);
    foreach my $me (@{$d{$type}{$key}}) { push @d, $me; }
  }

  for (my $i=0; $i<@d; $i++) {
    my $j = int(rand() * (@d-$i));
    print O $d[$j];
    $d[$j] = $d[$i];
    #print O $d[$i];
  }
  close O;
}
