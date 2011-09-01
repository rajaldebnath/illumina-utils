# -*- coding: utf-8 -*-
import sys

import fastqlib as u

def main(input_file_path, output_file_path, trim_to, compressed):
    input = u.FastQSource(input_file_path, compressed)
    output = u.FastQOutput(output_file_path, compressed)

    while input.next(trim_to = trim_to):
        if input.p_available:
            input.print_percentage()
        output.store(input.entry)

    sys.stderr.write('\n')
    return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Trim Illumina reads')
    parser.add_argument('-i', '--input', required=True, metavar = 'INPUT', help = 'FASTQ file to be trimmed')
    parser.add_argument('-l', '--length', required=True, type=int, metavar = 'LENGTH', help = 'Expected length of trimmed sequences')
    parser.add_argument('-o', '--output', help = 'Where trimmed sequences will be written (default: [-i]-TRIMMED-TO-[-l]')

    args = parser.parse_args()

    input_file_path = args.input
    
    compressed = input_file_path.endswith('.gz')
    
    if args.output:
        if compressed and not args.output.endswith('.gz'):
            output_file_path = args.output + '.gz'
        else:
            output_file_path = args.output
    else:
        if compressed:
            output_file_path = input_file_path[:-3] + '-TRIMMED-TO-%d.gz' % args.length 
        else:
            output_file_path = input_file_path + '-TRIMMED-TO-%d' % args.length

    sys.exit(main(input_file_path, output_file_path, args.length, compressed))
