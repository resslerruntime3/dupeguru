#import <Cocoa/Cocoa.h>
#import "PyApp.h"

@interface PyDupeGuruBase : PyApp
//Actions
- (NSNumber *)addDirectory:(NSString *)name;
- (void)removeDirectory:(NSNumber *)index;
- (void)setDirectory:(NSArray *)indexPath state:(NSNumber *)state;
- (void)loadResults;
- (void)saveResults;
- (void)loadIgnoreList;
- (void)saveIgnoreList;
- (void)clearIgnoreList;
- (void)purgeIgnoreList;
- (NSString *)exportToXHTMLwithColumns:(NSArray *)aColIds xslt:(NSString *)xsltPath css:(NSString *)cssPath;

- (NSNumber *)doScan;

- (void)selectPowerMarkerNodePaths:(NSArray *)aIndexPaths;
- (void)selectResultNodePaths:(NSArray *)aIndexPaths;

- (void)toggleSelectedMark;
- (void)markAll;
- (void)markInvert;
- (void)markNone;

- (void)addSelectedToIgnoreList;
- (void)refreshDetailsWithSelected;
- (void)removeSelected;
- (void)openSelected;
- (NSNumber *)renameSelected:(NSString *)aNewName;
- (void)revealSelected;
- (void)makeSelectedReference;
- (void)applyFilter:(NSString *)filter;

- (void)sortGroupsBy:(NSNumber *)aIdentifier ascending:(NSNumber *)aAscending;
- (void)sortDupesBy:(NSNumber *)aIdentifier ascending:(NSNumber *)aAscending;

- (void)copyOrMove:(NSNumber *)aCopy markedTo:(NSString *)destination recreatePath:(NSNumber *)aRecreateType;
- (void)deleteMarked;
- (void)removeMarked;

//Data
- (NSNumber *)getIgnoreListCount;
- (NSNumber *)getMarkCount;
- (NSString *)getStatLine;
- (NSNumber *)getOperationalErrorCount;

//Scanning options
- (void)setMinMatchPercentage:(NSNumber *)percentage;
- (void)setMixFileKind:(NSNumber *)mix_file_kind;
- (void)setDisplayDeltaValues:(NSNumber *)display_delta_values;
- (void)setEscapeFilterRegexp:(NSNumber *)escape_filter_regexp;
- (void)setRemoveEmptyFolders:(NSNumber *)remove_empty_folders;
- (void)setSizeThreshold:(int)size_threshold;
@end
