#!/usr/bin/env python

###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

"""
Map reads to GreenGenes database.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2013'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import os
import argparse
import ntpath

from readConfig import ReadConfig
from bwaUtils import mapPair, mapSingle

class MapReads(object):
  def __init__(self):
    self.ggDB = '/srv/db/gg/2013_05/gg_13_5_otus/rep_set/##_otus.fasta'
    pass

  def run(self, configFile, otu, threads):
    rc = ReadConfig()
    projectParams, sampleParams = rc.readConfig(configFile, outputDirExists = False)

    ggDB = self.ggDB.replace('##', str(otu), 1)
    print 'Mapping reads to the GreenGenes DB at: ' + ggDB + '\n'

    if not os.path.exists(ggDB + '.amb'):
      print 'Indexing GreenGenes DB:'
      os.system('bwa index -a is ' + ggDB)
      print ''
    else:
      print 'GreenGenes DB is already indexed.\n'

    for sample in sampleParams:
      print 'Mapping reads in sample: ' + sample

      pairs = sampleParams[sample]['pairs']
      singles = sampleParams[sample]['singles']

      # align and map each pair
      for i in xrange(0, len(pairs), 2):
        pair1 = pairs[i]
        pair2 = pairs[i+1]
        bamPrefix = projectParams['output_dir'] + ntpath.basename(pair1)
        mapPair(ggDB, pair1, pair2, bamPrefix, threads)

      # align and map each single-ended read file
      for i in xrange(0, len(singles)):
        bamPrefix = projectParams['output_dir'] + ntpath.basename(singles[i])
        mapSingle(ggDB, singles[i], bamPrefix, threads)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Map reads to GreenGenes database.",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('config_file', help='project config file')
  parser.add_argument('otu', help='clustering threshold of GreenGenes DB (choices: 94, 97, 99)', type=int, choices=[94, 97, 99])

  parser.add_argument('-t', '--threads', help='number of threads', type=int, default = 1)

  args = parser.parse_args()

  mapReads = MapReads()
  mapReads.run(args.config_file, args.otu, args.threads)
