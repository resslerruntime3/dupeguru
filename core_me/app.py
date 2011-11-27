# Created On: 2011/09/20
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.util import format_size, format_time

from core.app import (DupeGuru as DupeGuruBase, format_timestamp,
    format_perc, format_words, format_dupe_count, cmp_value)
from . import prioritize
from . import __appname__
from . import scanner, fs
from .result_table import ResultTable

class DupeGuru(DupeGuruBase):
    NAME = __appname__
    METADATA_TO_READ = ['size', 'mtime', 'duration', 'bitrate', 'samplerate', 'title', 'artist',
        'album', 'genre', 'year', 'track', 'comment']

    def __init__(self, view, appdata):
        DupeGuruBase.__init__(self, view, appdata)
        self.scanner = scanner.ScannerME()
        self.directories.fileclasses = [fs.MusicFile]
        self.result_table = ResultTable(self)
    
    def _get_display_info(self, dupe, group, delta):
        size = dupe.size
        duration = dupe.duration
        bitrate = dupe.bitrate
        samplerate = dupe.samplerate
        mtime = dupe.mtime
        m = group.get_match_of(dupe)
        if m:
            percentage = m.percentage
            dupe_count = 0
            if delta:
                r = group.ref
                size -= r.size
                duration -= r.duration
                bitrate -= r.bitrate
                samplerate -= r.samplerate
                mtime -= r.mtime
        else:
            percentage = group.percentage
            dupe_count = len(group.dupes)
        return {
            'name': dupe.name,
            'folder_path': str(dupe.folder_path),
            'size': format_size(size, 2, 2, False),
            'duration': format_time(duration, with_hours=False),
            'bitrate': str(bitrate),
            'samplerate': str(samplerate),
            'extension': dupe.extension,
            'mtime': format_timestamp(mtime,delta and m),
            'title': dupe.title,
            'artist': dupe.artist,
            'album': dupe.album,
            'genre': dupe.genre,
            'year': dupe.year,
            'track': str(dupe.track),
            'comment': dupe.comment,
            'percentage': format_perc(percentage),
            'words': format_words(dupe.words) if hasattr(dupe, 'words') else '',
            'dupe_count': format_dupe_count(dupe_count),
        }
    
    def _get_dupe_sort_key(self, dupe, get_group, key, delta):
        if key == 'percentage':
            m = get_group().get_match_of(dupe)
            return m.percentage
        if key == 'dupe_count':
            return 0
        r = cmp_value(dupe, key)
        if delta and (key in self.result_table.DELTA_COLUMNS):
            r -= cmp_value(get_group().ref, key)
        return r
    
    def _get_group_sort_key(self, group, key):
        if key == 'percentage':
            return group.percentage
        if key == 'dupe_count':
            return len(group)
        return cmp_value(group.ref, key)
    
    def _prioritization_categories(self):
        return prioritize.all_categories()
    
