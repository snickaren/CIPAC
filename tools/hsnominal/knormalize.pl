#!/usr/bin/perl
# Author: Kai Pöykiö
# 161116 v0.9
# For use with imagemagick histogram file (piped in, for now...)
# The result is black and white levels suitable for imagemagick's convert. 
# Removes some background noise and saturates text.
# It is useful for old typewriter written texts where some characters are
# unclear. Some slight increase of noise is expected but the recovery of unclear characters should outweigh this.

use POSIX;

$count_threshold = 0;
$similarity = 1.5;

@rgb_counts = ();

while (<STDIN>) {
	my ( $count, $R, $G, $B ) = /\s*(\d+)\s*:\s*\(\s*(\d+)\s*,\s*(\d)+\s*,\s*(\d+)\s*\)/o;

	if ( $count > $count_threshold ) {
		my $o = { 'c' => $count, 'r' =>$R, 'g'=>$G, 'b'=>$B, 'd' => 0 };
		$o->{'d'} = distance_colour($o);
		push @rgb_counts, $o;
	}
}

@sorted_counts = sort { $b->{'c'} <=> $a->{'c'} } @rgb_counts;
$top = $sorted_counts[0]->{'d'};
@sorted_counts = ();

@compacted_counts = @{compacted_distances(\@rgb_counts)};

sub maximums {

my @rgb_counts = @{shift @_};

while ( scalar @rgb_counts > 9 ) {

my $count = (scalar @rgb_counts) - 1;

my @localmaximums = ();

for my $index (0..$count) {
	my $c=$rgb_counts[$index]->{'c'};
	if ( ($rgb_counts[$index]->{'d'} > $top ) ) { next; }
	if ( $index-1 >= 0 ) {
		if ( abs($rgb_counts[$index]->{'d'} - $rgb_counts[$index-1]->{'d'}) < $similarity ) {
			$c_l1=$rgb_counts[$index-1]->{'c'};
		}
		else {
			$c_l1=-1;
		}
	}
	else {
		$c_l1 = 0.0;
	}
	if ( $index+1 <= $count ) {
		if ( abs($rgb_counts[$index]->{'d'} - $rgb_counts[$index+1]->{'d'}) < $similarity ) {
			$c_r1=$rgb_counts[$index+1]->{'c'};
		}
		else {
			$c_r1=-1;
		}
	}
	else {
		$c_r1=0.0;
	}

	if ( ($c_l1 == -1) && ($c_r1 == -1) ) {
		push @localmaximums, $rgb_counts[$index];
		next;
	}
	if ( $c_l1 == -1 ) {
		if ( $c > $c_r1 ) {
			push @localmaximums, $rgb_counts[$index];
			next;
		}
	}
	if ( $c_r1 == -1 ) {
		if ( $c > $c_l1 ) {
			push @localmaximums, $rgb_counts[$index];
			next;
		}
	}

	if ( ($c > $c_l1)  && ($c > $c_r1) ) {
		push @localmaximums, $rgb_counts[$index];
	}
}
	@rgb_counts = @localmaximums;

	if ( $count == (scalar @localmaximums) - 1 ) { last; }
}

return \@rgb_counts;
}


sub minimums {

my @rgb_counts = @{shift @_};

while ( scalar @rgb_counts > 9 ) {

my $count = (scalar @rgb_counts) - 1;

my @localminimums = ();

for my $index (0..$count) {
	my $c=$rgb_counts[$index]->{'c'};
	if ( ($rgb_counts[$index]->{'d'} > $top ) ) { next; }
	if ( $index-1 >= 0 ) {
		if ( abs($rgb_counts[$index]->{'d'} - $rgb_counts[$index-1]->{'d'}) < $similarity ) {
			$c_l1=$rgb_counts[$index-1]->{'c'};
		}
		else {
			$c_l1=-1;
		}
	}
	else {
		$c_l1 = 16000000;
	}
	if ( $index+1 <= $count ) {
		if ( abs($rgb_counts[$index]->{'d'} - $rgb_counts[$index+1]->{'d'}) < $similarity ) {
			$c_r1=$rgb_counts[$index+1]->{'c'};
		}
		else {
			$c_r1=-1;
		}
	}
	else {
		$c_r1 = 16000000;
	}

	if ( ($c_l1 == -1) && ($c_r1 == -1) ) {
		push @localminimums, $rgb_counts[$index];
		next;
	}
	if ( $c_l1 == -1 ) {
		if ( $c <= $c_r1 ) {
			push @localminimums, $rgb_counts[$index];
			next;
		}
	}
	if ( $c_r1 == -1 ) {
		if ( $c <= $c_l1 ) {
			push @localminimums, $rgb_counts[$index];
			next;
		}
	}

	if ( (($c <= $c_l1)  && ($c < $c_r1)) || (($c < $c_l1)  && ($c <= $c_r1)) ) {
		push @localminimums, $rgb_counts[$index];
	}
}

@rgb_counts = @localminimums;

if ( $count == (scalar @localminimums) - 1 ) { last; }
}

return \@rgb_counts;
}

sub distance_colour {
	my ($c) = shift @_;

	my $distance = (((($c->{'r'}**2)+($c->{'g'}**2)+($c->{'b'}**2)) ** 0.5) / ((255*255*3)**0.5))*100;

	return $distance;
}

sub compacted_distances {

my @rgb_counts = @{shift @_};
my %compacted = ();
my $count = (scalar @rgb_counts)-1;

for my $i (0..$count) {
	my $c = $rgb_counts[$i]->{'c'};
	my $d = floor($rgb_counts[$i]->{'d'});
	if ( defined $compacted{$d} ) {
		$compacted{$d} += $c;
	}
	else {
		$compacted{$d} = $c;
	}
}

my @result = ();

for my $i (sort { $a <=> $b } keys %compacted ) {
	push @result, {'d'=>$i, 'c'=>$compacted{$i}};
}

return \@result;
}

@counts = @{maximums(\@compacted_counts)};
$low_max = $counts[0]->{'d'};

@counts = @{minimums(\@compacted_counts)};
$count = (scalar @counts) - 1;
for my $i (0..$count) {
	if ($counts[$i]->{'d'} > $low_max ) {
		$min = $counts[$i]->{'d'};
		last;
	}
}

$max = $counts[$count]->{'d'};
$sum=0.0;
$sum_count=0.0;
for my $o (@rgb_counts) {
	if (floor($o->{'d'}) == $max) {
		$sum+=$o->{'d'}*$o->{'c'};
		$sum_count+=$o->{'c'};
	}
}
$max = $sum/$sum_count;

my $sum = 0.0;
my $sum_count = 0.0;
$count = (scalar @rgb_counts) - 1;
for my $index (0..$count) {
	if ( $rgb_counts[$index]->{'d'} > $max ) { next; };
	if ( $rgb_counts[$index]->{'d'} < $min+1 ) { next; };
	$sum += $rgb_counts[$index]->{'d'}*$rgb_counts[$index]->{'c'};		
	$sum_count += $rgb_counts[$index]->{'c'};
}

my $white_pct = $top;
my $black_pct = $sum/$sum_count;
$black_pct += ($max-$black_pct)*0.89;

print $black_pct, ',', $white_pct; 
