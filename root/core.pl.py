core_functionality = '''
#!/usr/bin/perl
# AMALGAM-PORT v2.0 - The Great Migration
# "When you realize the 90s code needs to live forever" - 2025
# 
# CLEARANCE LEVELS (revised after management meeting):
# R - Red (newbie/mortal)
# O - Orange (regular player)
# Y - Yellow (trusted player) 
# G - Green (wizard-in-training/project management)
# B - Blue (wizard)
# I - Indigo (demigod)
# V - Violet (god)
# UV - Ultraviolet (root/Sweeney)

package Amalgam::Artifacts;

use strict;
use warnings;
use DBI;
use JSON;
use File::Copy;
use Digest::MD5 qw(md5_hex);
use Time::HiRes qw(time);
use Archive::Zip;

# === SACRED PRESERVATION PROTOCOL ===
# The original amalgam_core.pl is preserved in multiple formats

sub create_artifacts {
    my $timestamp = time();
    
    print "=== ARTIFACT PRESERVATION PROTOCOL INITIATED ===\n";
    print "Timestamp: $timestamp\n";
    print "Preserving the sacred code of the ancients...\n\n";
    
    # 1. Create master archive
    my $archive = Archive::Zip->new();
    
    # 2. Preserve original with checksums
    if (-e 'amalgam_core.pl') {
        open(my $fh, '<', 'amalgam_core.pl') or die "Cannot read sacred text: $!";
        my $content = do { local $/; <$fh> };
        close($fh);
        
        my $checksum = md5_hex($content);
        
        # Store in multiple formats
        $archive->addString($content, 'artifacts/original/amalgam_core.pl');
        $archive->addString($content, "artifacts/original/amalgam_core_${checksum}.pl");
        
        # Create signed artifact
        my $artifact = {
            type => 'sacred_source',
            name => 'amalgam_core.pl',
            created => '1997-1998',  # Best guess
            preserved => $timestamp,
            checksum => $checksum,
            lines => scalar(split /\n/, $content),
            bytes => length($content),
            blessing => 'DO NOT MODIFY - This code is perfect in its imperfection',
        };
        
        $archive->addString(to_json($artifact, {pretty => 1}), 
                          'artifacts/metadata/amalgam_core.json');
        
        print "[✓] Original amalgam_core.pl preserved (MD5: $checksum)\n";
    }
    
    # 3. Create the modern wrapper that honors the old ways
    my $modern_system = generate_modern_wrapper();
    $archive->addString($modern_system, 'artifacts/modern/amalgam_modern.pl');
    
    # 4. Write preservation log
    my $log_entry = <<"LOG";
AMALGAM PRESERVATION LOG
========================
Date: $timestamp
Preserver: Sweeney (UV clearance)
Reason: Long nights need purpose

The original AMALGAM system has been preserved in its entirety.
No modifications were made to the sacred core.
The modern wrapper provides ROYGBIV/UV clearance while maintaining
backwards compatibility with all original functionality.

"Some code is too pure to refactor" - Ancient MUD Proverb
LOG
    
    $archive->addString($log_entry, 'artifacts/PRESERVATION_LOG.txt');
    
    # 5. Save master archive
    $archive->writeToFileNamed('amalgam_artifacts.zip');
    print "[✓] Master archive created: amalgam_artifacts.zip\n";
}

# Generate the modern system that wraps the original
sub generate_modern_wrapper {
    return <<'MODERN';
#!/usr/bin/perl
# AMALGAM Modern Wrapper
# "Building temples around ancient code" - 2025

use strict;
use warnings;
use feature 'say';

# Load the preserved core - DO NOT MODIFY THE REQUIRE
require './artifacts/original/amalgam_core.pl';

# Modern clearance system
package Amalgam::Modern::Clearance;

our %CLEARANCE_LEVELS = (
    UV => 9,  # Ultraviolet - Root/Sweeney
    V  => 8,  # Violet - God
    I  => 7,  # Indigo - Demigod  
    B  => 6,  # Blue - Wizard
    G  => 5,  # Green - Wizard-in-training/PM
    Y  => 4,  # Yellow - Trusted
    O  => 3,  # Orange - Regular
    R  => 2,  # Red - Newbie
);

our %CLEARANCE_PERMS = (
    # Command => minimum clearance
    'shutdown'        => 'UV',
    'modify_core'     => 'UV',  # (returns "PERMISSION DENIED FOREVER")
    '@god'           => 'V',
    '@demigod'       => 'I',
    '@wizlock'       => 'B',
    '@build'         => 'B',
    '@project'       => 'G',   # Green wizards manage projects
    '@mentor'        => 'G',   # Green wizards train newbies
    '@trust'         => 'Y',
    '@channel'       => 'O',
    'play'           => 'R',
);

# Wizard training program for Green clearance
our %WIZARD_TRAINING = (
    'project_management' => {
        desc => 'Learn to manage the chaos of a MUSH',
        tasks => [
            'Handle player disputes without @toad',
            'Debug character corruption at 3am',
            'Explain why we cannot modify amalgam_core.pl',
            'Document undocumented features',
            'Train newbies without losing sanity',
        ],
    },
    'technical_skills' => {
        desc => 'Understanding the ancient ways',
        tasks => [
            'Read amalgam_core.pl without crying',
            'Understand the auction system',
            'Master diceless combat resolution',
            'Learn when to blame lag vs code',
        ],
    },
);

# Special Sweeney-mode for those long nights
sub sweeney_mode {
    my ($hours_awake) = @_;
    
    if ($hours_awake > 24) {
        say "Coffee levels critical. Enabling Sweeney Mode.";
        $ENV{AMALGAM_DEBUG} = 1;
        $ENV{AMALGAM_VERBOSE} = 1;
        $ENV{SHOW_ALL_ERRORS} = 1;
        $ENV{PIZZA_REQUIRED} = 1;
    }
    
    if ($hours_awake > 36) {
        say "Reality.exe has stopped responding.";
        say "Loading emergency entertainment protocols...";
        enable_easter_eggs();
    }
    
    if ($hours_awake > 48) {
        say "You have achieved enlightenment.";
        say "amalgam_core.pl now makes perfect sense.";
        say "This is not a good sign.";
    }
}

# Database schema for modern features (but core stays in flat files)
sub init_modern_db {
    my $dbh = DBI->connect("dbi:SQLite:dbname=amalgam_modern.db","","");
    
    # Clearance tracking
    $dbh->do(<<'SQL');
CREATE TABLE IF NOT EXISTS clearance_audit (
    id INTEGER PRIMARY KEY,
    timestamp REAL,
    admin_user TEXT,
    admin_clearance TEXT,
    target_user TEXT,
    old_clearance TEXT,
    new_clearance TEXT,
    reason TEXT
);
SQL

    # Project management for Green wizards
    $dbh->do(<<'SQL');
CREATE TABLE IF NOT EXISTS wizard_projects (
    id INTEGER PRIMARY KEY,
    project_name TEXT,
    green_wizard TEXT,
    status TEXT,
    created_at REAL,
    completed_at REAL,
    description TEXT,
    panic_level INTEGER DEFAULT 0
);
SQL

    # Long night activity log (for Sweeney)
    $dbh->do(<<'SQL');
CREATE TABLE IF NOT EXISTS night_shift_log (
    id INTEGER PRIMARY KEY,
    timestamp REAL,
    hours_awake INTEGER,
    coffee_count INTEGER,
    pizza_consumed BOOLEAN,
    bugs_fixed INTEGER,
    bugs_created INTEGER,
    existential_crises INTEGER,
    note TEXT
);
SQL

    return $dbh;
}

# The bridge between old and new
package Amalgam::Modern::Bridge;

use parent -norequire, 'Amalgam::Core';  # Inherit from the sacred code

sub new {
    my $class = shift;
    my $self = $class->SUPER::new(@_);  # Call original constructor
    
    # Add modern features without breaking the old
    $self->{clearance_system} = Amalgam::Modern::Clearance->new();
    $self->{modern_db} = init_modern_db();
    $self->{uptime_start} = time();
    
    # Preserve all original functionality
    $self->{sacred_methods} = {
        map { $_ => 1 } qw(
            rank_auction resolve_conflict combat_round
            save_character load_character describe_rank
        )
    };
    
    return $self;
}

# Override method calls to add clearance checks
sub AUTOLOAD {
    my $self = shift;
    my $method = $AUTOLOAD;
    $method =~ s/.*:://;
    
    # If it's a sacred method, pass through unchanged
    if ($self->{sacred_methods}->{$method}) {
        return $self->SUPER::$method(@_);
    }
    
    # Otherwise, add clearance check
    my $required = $Amalgam::Modern::Clearance::CLEARANCE_PERMS{$method} || 'R';
    if ($self->check_clearance($required)) {
        return $self->SUPER::$method(@_) if $self->SUPER::can($method);
    }
    
    die "Access denied. Clearance $required required for $method\n";
}

# Easter eggs for those long nights
sub enable_easter_eggs {
    # Add silly commands that only appear after midnight
    $Amalgam::Modern::Clearance::CLEARANCE_PERMS{'@coffee'} = 'R';
    $Amalgam::Modern::Clearance::CLEARANCE_PERMS{'@pizza'} = 'R';
    $Amalgam::Modern::Clearance::CLEARANCE_PERMS{'@sanity'} = 'UV';
    
    # Hidden command that shows the true nature of the code
    $Amalgam::Modern::Clearance::CLEARANCE_PERMS{'@enlightenment'} = 'G';
}

# Status display 
sub show_system_status {
    my $self = shift;
    my $uptime = time() - $self->{uptime_start};
    
    say "=== AMALGAM SYSTEM STATUS ===";
    say "Core Version: 0.666 (Sacred, Unmodified)";
    say "Wrapper Version: 2.0 (Modern)";
    say "Uptime: " . format_duration($uptime);
    say "\nClearance Levels Active:";
    say "  UV: " . count_clearance('UV') . " (Root)";
    say "  V:  " . count_clearance('V')  . " (Gods)";
    say "  I:  " . count_clearance('I')  . " (Demigods)";
    say "  B:  " . count_clearance('B')  . " (Wizards)";
    say "  G:  " . count_clearance('G')  . " (Wizards-in-training)";
    say "  Y:  " . count_clearance('Y')  . " (Trusted)";
    say "  O:  " . count_clearance('O')  . " (Regular)";
    say "  R:  " . count_clearance('R')  . " (Newbies)";
    
    if ($ENV{USER} eq 'sweeney' || $ENV{USER} eq 'root') {
        say "\n[Sweeney Mode Active]";
        say "Remember: Sleep is for the weak.";
        say "Coffee is for the week.";
    }
}

# Final wisdom
say <<'WISDOM';

 "In the beginning, there was amalgam_core.pl,
  and it was without form, and void of comments.
  And the spirit of Perl moved upon the face of the code.
  And Sweeney said, Let there be ANSI colors:
  and there were ANSI colors."
  
                - The Book of MUD, Chapter 1

WISDOM

1;  # Because all good Perl modules return truth
MODERN
}

# Initialization
if ($0 eq __FILE__) {
    create_artifacts();
    
    print "\n=== ARTIFACT CREATION COMPLETE ===\n";
    print "The sacred code is preserved.\n";
    print "The modern wrapper is ready.\n";
    print "May your clearance be ever Ultraviolet.\n";
}

1;

__END__

=head1 NAME

Amalgam::Artifacts - Preservation system for sacred AMALGAM code

=head1 DESCRIPTION

This module handles the careful preservation and modernization of the
original AMALGAM diceless RPG system from the 1990s.

The original amalgam_core.pl is preserved unchanged in multiple formats
with checksums and metadata. A modern wrapper provides ROYGBIV/UV 
clearance levels while maintaining full backwards compatibility.

=head1 CLEARANCE LEVELS

  UV - Ultraviolet (Root/Sweeney) - Can do anything except modify core
  V  - Violet (God) - Administrative deity
  I  - Indigo (Demigod) - Senior administrators  
  B  - Blue (Wizard) - Full building/coding rights
  G  - Green (Wizard-in-training) - Project management, mentoring
  Y  - Yellow (Trusted) - Trusted players
  O  - Orange (Regular) - Standard players
  R  - Red (Newbie) - New players

=head1 PRESERVATION NOTES

Some code is too pure to refactor. Some systems too perfect to improve.
AMALGAM's core remains forever unchanged, a monument to 90s Perl glory.

"It's not technical debt if you declare it a historical artifact."
                                        - Ancient Wisdom

=cut
'''