from const import files


def main():
    with open('oldws.txt', 'r') as source, open(files.SOURCE, 'w') as target:
        for line in source:
            if any(map(line.startswith, ignore)):
                target.write(line)
            elif line.startswith('// Mags'):
                continue
            elif line.startswith('// Overall'):
                barrels = None
                source.readline()
            elif line.startswith('//'):
                target.write(process_line(line))
                barrels = line.split(' | ')[1].strip()
            elif line.startswith('/'):
                target.write(f'{line} | {barrels}')
            else:
                target.write(line)


def process_line(line):
    global barrels
    line = line.strip()
    output = ''
    if line.startswith('// Name'):
        line = line.replace('// Name N ', '', 1).replace('// Name E ', '', 1)
        data = line.split(' | ')
        weapon = data[0]
        output = f'// {weapon}\n'
        barrels = data[1]
        return output
    elif line.startswith('// Usage'):
        line = line.replace("// Usage ", '')
        data = line.split(' | ')
        output = f'/{data[0]}: {data[1]} | {barrels}\n'
        return output
    elif line.startswith('// Perks '):
        line = line.replace('// Perks ', '', 1)
        data = line.split(' | ')
        traits = data[0].split()
        output = f'Roll: {data[1]} | {traits[1]} {traits[0]}\n'
        return output


ignore = ['--', '##', 'title:', 'description:']
barrels = None

if __name__ == "__main__":
    main()


"""
// Name E Thoughtless | ArrowheadBrake ExtendedBarrel ChamberedCompensator FlutedBarrel

// Usage PvE | Stability ReloadSpeed
// Perks FiringLine Overflow | AppendedMag TacticalMag
// Perks FocusedFury Overflow | AppendedMag TacticalMag
// Perks FiringLine RapidHit | AppendedMag TacticalMag
// Mags

// Usage PvP | Stability Range
// Perks SnapshotSights PerpetualMotion | AccuricedRounds TacticalMag
// Perks SnapshotSights FirmlyPlanted | AccuricedRounds TacticalMag
// Mags

// Overall
"""

# zu

"""
--------------------------------------------------
##Kategorie
--------------------------------------------------

// PieceOfMind

/PvE: Stability | ArrowheadBrake ChamberedCompensator CorkscrewRifling ExtendedBarrel
Roll: HighCaliberRounds RicochetRounds | Overflow VorpalWeapon
Roll: HighCaliberRounds RicochetRounds | Overflow Harmony

/PvP: Range | ArrowheadBrake ChamberedCompensator CorkscrewRifling ExtendedBarrel
Roll: HighCaliberRounds RicochetRounds | PerpetualMotion MovingTarget
"""
