typedef unsigned char   undefined;

typedef unsigned char    bool;
typedef unsigned int    dword;
typedef long long    longlong;
typedef int    sdword;
typedef unsigned char    uchar;
typedef unsigned int    uint;
typedef unsigned long long    ulonglong;
typedef unsigned char    undefined1;
typedef unsigned int    undefined4;
typedef unsigned short    ushort;
#define unkbyte9   unsigned long long
#define unkbyte10   unsigned long long
#define unkbyte11   unsigned long long
#define unkbyte12   unsigned long long
#define unkbyte13   unsigned long long
#define unkbyte14   unsigned long long
#define unkbyte15   unsigned long long
#define unkbyte16   unsigned long long

#define unkuint9   unsigned long long
#define unkuint10   unsigned long long
#define unkuint11   unsigned long long
#define unkuint12   unsigned long long
#define unkuint13   unsigned long long
#define unkuint14   unsigned long long
#define unkuint15   unsigned long long
#define unkuint16   unsigned long long

#define unkint9   long long
#define unkint10   long long
#define unkint11   long long
#define unkint12   long long
#define unkint13   long long
#define unkint14   long long
#define unkint15   long long
#define unkint16   long long

#define unkfloat1   float
#define unkfloat2   float
#define unkfloat3   float
#define unkfloat5   double
#define unkfloat6   double
#define unkfloat7   double
#define unkfloat9   long double
#define unkfloat11   long double
#define unkfloat12   long double
#define unkfloat13   long double
#define unkfloat14   long double
#define unkfloat15   long double
#define unkfloat16   long double

#define BADSPACEBASE   void
#define code   void

typedef struct section section, *Psection;

struct section {
    char sectname[16];
    char segname[16];
    dword addr;
    dword size;
    dword offset;
    dword align;
    dword reloff;
    dword nrelocs;
    dword flags;
    dword reserved1;
    dword reserved2;
};

typedef struct dysymtab_command dysymtab_command, *Pdysymtab_command;

struct dysymtab_command {
    dword cmd;
    dword cmdsize;
    dword ilocalsym;
    dword nlocalsym;
    dword iextdefsym;
    dword nextdefsym;
    dword iundefsym;
    dword nundefsym;
    dword tocoff;
    dword ntoc;
    dword modtaboff;
    dword nmodtab;
    dword extrefsymoff;
    dword nextrefsyms;
    dword indirectsymoff;
    dword nindirectsyms;
    dword extreloff;
    dword nextrel;
    dword locreloff;
    dword nlocrel;
};

typedef struct segment_command segment_command, *Psegment_command;

struct segment_command {
    dword cmd;
    dword cmdsize;
    char segname[16];
    dword vmaddr;
    dword vmsize;
    dword fileoff;
    dword filesize;
    dword maxprot;
    dword initprot;
    dword nsects;
    dword flags;
};

typedef struct symtab_command symtab_command, *Psymtab_command;

struct symtab_command {
    dword cmd;
    dword cmdsize;
    dword symoff;
    dword nsyms;
    dword stroff;
    dword strsize;
};

typedef struct version_min_command version_min_command, *Pversion_min_command;

struct version_min_command {
    dword cmd;
    dword cmdsize;
    dword version;
    dword sdk;
};

typedef struct mach_header mach_header, *Pmach_header;

struct mach_header {
    dword magic;
    dword cputype;
    dword cpusubtype;
    dword filetype;
    dword ncmds;
    dword sizeofcmds;
    dword flags;
};

typedef struct linkedit_data_command linkedit_data_command, *Plinkedit_data_command;

struct linkedit_data_command {
    dword cmd;
    dword cmdsize;
    dword dataoff;
    dword datasize;
};

typedef uchar uint8;

typedef ulonglong s3e_uint64_t;

typedef dword uint32;

typedef longlong s3e_int64_t;

typedef short s3e_int16_t;

typedef uint uintptr_t;

typedef ushort s3e_uint16_t;

typedef int intptr_t;

typedef ulonglong sizetype;

typedef sdword int32;

typedef char int8;

typedef enum s3eDeviceState {
    S3E_DEVICE_STATE_PAUSED=3,
    S3E_DEVICE_STATE_EXITING=4,
    S3E_DEVICE_STATE_RUNNING=5
} s3eDeviceState;

typedef enum s3eDeviceArchitecture {
    S3E_DEVICE_ARCHITECTURE_UNKNOWN=-1,
    S3E_DEVICE_ARCHITECTURE_ARM4T=0,
    S3E_DEVICE_ARCHITECTURE_ARM4=1,
    S3E_DEVICE_ARCHITECTURE_ARM5T=2,
    S3E_DEVICE_ARCHITECTURE_ARM5TE=3,
    S3E_DEVICE_ARCHITECTURE_ARM5TEJ=4,
    S3E_DEVICE_ARCHITECTURE_ARM6=5,
    S3E_DEVICE_ARCHITECTURE_ARM6K=6,
    S3E_DEVICE_ARCHITECTURE_ARM6T2=7,
    S3E_DEVICE_ARCHITECTURE_ARM6Z=8,
    S3E_DEVICE_ARCHITECTURE_X86=9,
    S3E_DEVICE_ARCHITECTURE_PPC=10,
    S3E_DEVICE_ARCHITECTURE_AMD64=11,
    S3E_DEVICE_ARCHITECTURE_X86_64=11,
    S3E_DEVICE_ARCHITECTURE_ARM7A=12,
    S3E_DEVICE_ARCHITECTURE_ARM8A=14,
    S3E_DEVICE_ARCHITECTURE_ARM8A_AARCH64=15,
    S3E_DEVICE_ARCHITECTURE_NACLX86_64=16,
    S3E_DEVICE_ARCHITECTURE_MAX=17
} s3eDeviceArchitecture;

typedef enum s3eDeviceSoftKeyPosition {
    S3E_DEVICE_SOFTKEY_BOTTOM_LEFT=0,
    S3E_DEVICE_SOFTKEY_BOTTOM_RIGHT=1,
    S3E_DEVICE_SOFTKEY_TOP_RIGHT=2,
    S3E_DEVICE_SOFTKEY_TOP_LEFT=3
} s3eDeviceSoftKeyPosition;

typedef struct _s3eSymbolsInfo _s3eSymbolsInfo, *P_s3eSymbolsInfo;

typedef struct _s3eSymbolsInfo s3eSymbolsInfo;

typedef struct IwS3EHashtable IwS3EHashtable, *PIwS3EHashtable;

typedef struct IwS3EHashEntry IwS3EHashEntry, *PIwS3EHashEntry;

typedef s3e_uint16_t uint16_t;

typedef uint16_t uint16;

struct _s3eSymbolsInfo {
    int m_Num;
    char **m_Names;
    uint32 *m_Hashes;
    void **m_FnPtrs;
    uint8 *m_Attribs;
    void **m_FnPtrsOrig;
    struct IwS3EHashtable *m_AddrHashtable;
};

struct IwS3EHashtable {
    struct IwS3EHashEntry *m_Table[1024];
    struct IwS3EHashEntry *m_Entries;
};

struct IwS3EHashEntry {
    struct IwS3EHashEntry *m_Next;
    uint16 m_Symbol;
};

typedef struct _s3eThread _s3eThread, *P_s3eThread;

typedef struct _s3eThread s3eThread;

typedef struct s3eThreadSys s3eThreadSys, *Ps3eThreadSys;

typedef uint8 s3eBool;

typedef void (*s3eThreadCleanupHandler)(void);

typedef struct s3eTLSGlobals s3eTLSGlobals, *Ps3eTLSGlobals;

struct s3eThreadSys {
};

struct _s3eThread {
    struct s3eThreadSys *m_ThreadSys;
    s3eBool m_Detached;
    s3eBool m_Cancelled;
    s3eBool m_DoneCancel;
    s3eBool m_Exited;
    s3eBool m_Suspended;
    s3eBool m_Internal;
    void *m_ExitCode;
    s3eThreadCleanupHandler m_CleanupHandler;
    struct s3eTLSGlobals *m_TLSGlobals;
};

struct s3eTLSGlobals {
    s3eThread *m_Thread;
    void *m_DeviceTLS;
    void *m_StackSwitchTLS;
};

typedef struct s3eExecGlobals s3eExecGlobals, *Ps3eExecGlobals;

typedef struct s3eExecHandle s3eExecHandle, *Ps3eExecHandle;

typedef struct CS3EExecStack CS3EExecStack, *PCS3EExecStack;

typedef struct IwS3E IwS3E, *PIwS3E;

typedef s3e_uint64_t uint64_t;

typedef uint64_t uint64;

typedef int jmp_buf[28];

typedef struct s3eFibre s3eFibre, *Ps3eFibre;

typedef struct entry entry, *Pentry;

typedef int32 (*IwS3EDataFunc)(void *, int32, void *);

typedef struct IwS3EHeader IwS3EHeader, *PIwS3EHeader;

typedef struct IwS3EExtHeader IwS3EExtHeader, *PIwS3EExtHeader;

typedef struct s3eSHA1 s3eSHA1, *Ps3eSHA1;

typedef void * (*s3eFibreFunc)(void *);

typedef s3e_int64_t int64_t;

typedef int64_t int64;

typedef void *__builtin_va_list;

typedef __builtin_va_list va_list;

typedef int64 (*s3eFibreCallFunc)(int, va_list);

typedef s3e_int16_t int16_t;

typedef int16_t int16;

struct entry {
    char m_Name[128];
    char m_Root[256];
    char *m_ConfigAppend;
    char *m_ConfigPrepend;
};

struct IwS3EExtHeader {
    int32 m_HeaderSize;
    int32 m_DataOffset;
    int32 m_IsJuice;
};

struct s3eSHA1 {
};

struct s3eFibre {
    void *m_CurrentStack;
    void *m_Stack;
    int m_StackSize;
    s3eBool m_StackGuard;
    s3eBool m_StackOwned;
    undefined field5_0xe;
    undefined field6_0xf;
    s3eFibreFunc m_StartFn;
    void *m_Param;
    void *m_Return;
    s3eBool m_Finished;
    undefined field11_0x1d;
    undefined field12_0x1e;
    undefined field13_0x1f;
    struct s3eFibre *m_Parent;
    struct s3eFibre *m_FibreCaller;
    s3eFibreCallFunc m_FibreCall;
    int m_FibreCallArgc;
    va_list m_FibreCallArgs;
    int64 m_FibreCallRet;
};

struct IwS3EHeader {
    int32 m_Ident;
    int32 m_Version;
    int16 m_Flags;
    int16 m_Architecture;
    int32 m_FixupOffset;
    int32 m_FixupSize;
    int32 m_CodeOffset;
    int32 m_CodeFileSize;
    int32 m_CodeMemSize;
    int32 m_SigOffset;
    int32 m_SigSize;
    int32 m_Entry;
    int32 m_ConfigOffset;
    int32 m_ConfigSize;
    int32 m_BaseAddress;
    int32 m_ExtraSectionOffset;
    int32 m_ExtraSectionSize;
};

struct IwS3E {
    char m_FileName[128];
    IwS3EDataFunc m_ReadFunc;
    int m_BytesRead;
    struct IwS3EHeader m_Header;
    struct IwS3EExtHeader m_ExtHeader;
    void *m_UserData;
    uint8 *m_Fixup;
    uint8 *m_CodeSegment;
    int m_TotalCodeSize;
    uint8 *m_Code;
    int m_CodeSize;
    uint8 *m_Data;
    int m_DataSize;
    uint8 *m_Signature;
    uint8 *m_ExtraSection;
    struct IwS3EHashtable *m_Hashtable;
    uint8 *m_Veneers;
    int m_VeneersSize;
    int m_VeneerSize;
    struct s3eSHA1 *m_HashCtx;
    bool m_bReadHash;
};

struct CS3EExecStack {
    int m_LastIndex;
    struct entry m_Stack[3];
};

struct s3eExecGlobals {
    struct s3eExecHandle *g_LoadedS3E;
    s3eSymbolsInfo g_SymInfo;
    struct CS3EExecStack g_ExecStack;
    struct IwS3E *g_CurS3E;
    int32 g_GlobalServices;
    int g_ExecCount;
    bool g_S3ELoadAborted;
    bool g_DoneStartup;
    undefined field8_0x4ca;
    undefined field9_0x4cb;
    uint64 g_StartupTime;
    bool g_IsNonEval;
    bool g_IsJuiceInLicense;
    bool g_LicenseLoaded;
    char g_LicType[64];
    undefined field15_0x517;
    char *g_LicText;
    s3eBool g_SplashDone;
    s3eBool g_BrandSplash;
    s3eBool g_FreeLicense;
    undefined field20_0x51f;
    int g_LastExitCode;
    int g_LastCodeDataSize;
    bool g_ClearedTraceFile;
    s3eBool g_HideBackwardsMessage;
    undefined field25_0x52a;
    undefined field26_0x52b;
    struct s3eThreadSys *g_OSThread;
    struct s3eThreadSys *g_MainThread;
    jmp_buf g_setjmpBuffer;
    struct s3eFibre *g_LoaderFibre;
    uint32 g_CodeHash;
};

struct s3eExecHandle {
};

typedef struct IwS3EInternalReloc IwS3EInternalReloc, *PIwS3EInternalReloc;

struct IwS3EInternalReloc {
    int32 m_Offset;
};

typedef struct IwS3EMetaHeader IwS3EMetaHeader, *PIwS3EMetaHeader;

struct IwS3EMetaHeader {
    int32 m_S3EHeaderOffset;
    int32 m_S3EExtHeaderOffset;
    int32 m_ConfigOffset;
    int32 m_ConfigSize;
    int32 m_SymbolsOffset;
    int32 m_SymbolsSize;
    int32 m_RelocationsOffset;
    int32 m_RelocationsSize;
    int32 m_SigOffset;
    int32 m_SigSize;
    int32 m_LicenseOffset;
    int32 m_LicenseSize;
};

typedef struct IwS3EFixupSectionHdr IwS3EFixupSectionHdr, *PIwS3EFixupSectionHdr;

struct IwS3EFixupSectionHdr {
    int32 m_Type;
    int32 m_Size;
};

typedef struct IwS3EExternalRelocSection IwS3EExternalRelocSection, *PIwS3EExternalRelocSection;

typedef struct IwS3EExternalReloc IwS3EExternalReloc, *PIwS3EExternalReloc;

struct IwS3EExternalReloc {
    uint16 m_Offset_hi;
    uint16 m_Offset_lo;
    uint16 m_SymbolIdx;
};

struct IwS3EExternalRelocSection {
    struct IwS3EFixupSectionHdr m_Hdr;
    int32 m_NumRelocs;
    struct IwS3EExternalReloc m_Relocs[1];
};

typedef struct IwS3ESymbolsSection IwS3ESymbolsSection, *PIwS3ESymbolsSection;

struct IwS3ESymbolsSection {
    struct IwS3EFixupSectionHdr m_Hdr;
    int16 m_NumSymbols;
    int8 m_Symbols[1];
};

typedef struct IwS3EInternalRelocSection IwS3EInternalRelocSection, *PIwS3EInternalRelocSection;

struct IwS3EInternalRelocSection {
    struct IwS3EFixupSectionHdr m_Hdr;
    int32 m_NumRelocs;
    struct IwS3EInternalReloc m_Relocs[1];
};

typedef struct IwS3EAdditionalData IwS3EAdditionalData, *PIwS3EAdditionalData;

struct IwS3EAdditionalData {
    uint32 m_Size;
    uint32 m_Type;
};

typedef enum IwS3EFlags {
    IW_S3E_DEBUG_F=1,
    IW_S3E_GCC_F=2,
    IW_S3E_RVCT_F=4,
    IW_S3E_PIE_F=8,
    IW_S3E_64BIT_F=16
} IwS3EFlags;

typedef struct s3eDeviceGlobals s3eDeviceGlobals, *Ps3eDeviceGlobals;

typedef enum s3eErrorPriority {
    S3E_ERROR_PRI_MINOR=0,
    S3E_ERROR_PRI_NORMAL=1,
    S3E_ERROR_PRI_MAJOR=2,
    S3E_ERROR_PRI_MAX=3
} s3eErrorPriority;

typedef intptr_t s3eThreadTLS;

typedef struct s3eThreadSemSys s3eThreadSemSys, *Ps3eThreadSemSys;

typedef struct s3eThreadLockSys s3eThreadLockSys, *Ps3eThreadLockSys;

typedef enum s3eDeviceOrientation {
    S3E_DEVICE_ORIENTATION_NORMAL=0,
    S3E_DEVICE_ORIENTATION_ROT90=1,
    S3E_DEVICE_ORIENTATION_ROT180=2,
    S3E_DEVICE_ORIENTATION_ROT270=3
} s3eDeviceOrientation;

struct s3eThreadLockSys {
};

struct s3eThreadSemSys {
};

struct s3eDeviceGlobals {
    uint64 g_LastPumpMessageTime;
    uint64 g_LastTimerTick;
    int32 g_ErrorTraceLevel;
    uint8 g_ExitCode;
    uint8 g_LastExitCode;
    uint8 g_ExitSignal;
    uint8 g_LastExitSignal;
    uint32 g_LastPowerConnectionTestTime;
    void *g_LoadAddress;
    uint64 g_LastYieldTime;
    s3eThread *g_SuspendingThread;
    uint32 g_NextErrorDevice;
    int32 g_NextError;
    enum s3eErrorPriority g_NextErrorPriority;
    s3eThreadTLS g_DeviceTLS;
    s3eBool g_SuspendGLOnly;
    s3eBool g_SuspendSignaled;
    s3eBool g_EnterSuspend;
    s3eBool g_TestSuspendResume;
    struct s3eThreadSemSys *g_SuspendedNotify;
    int g_SuspendedThreads;
    struct s3eThreadSemSys *g_ResumedNotify;
    uint32 g_InitServices;
    s3eBool g_RequestPause;
    s3eBool g_RequestQuit;
    s3eBool g_HandleCPUExceptions;
    undefined field26_0x53;
    enum s3eDeviceState g_DeviceState;
    s3eBool g_EndKeyPressed;
    s3eBool g_TraceErrors;
    s3eBool g_APITrace;
    s3eBool g_AppIsRunning;
    int g_DeviceArch;
    int g_DeviceVFP;
    uint8 g_GameVersionMajor;
    uint8 g_GameVersionMinor;
    undefined field36_0x66;
    undefined field37_0x67;
    enum s3eDeviceArchitecture g_GameArch;
    s3eBool g_GameVFP;
    s3eBool g_NoMixSoundAudio;
    char g_StringPropBuffer[64];
    undefined field42_0xae;
    undefined field43_0xaf;
    enum s3eDeviceSoftKeyPosition g_BackSoftKeyPosition;
    enum s3eDeviceSoftKeyPosition g_AdvanceSoftKeyPosition;
    struct s3eThreadLockSys *g_GlobalLock;
    int32 g_PushNotificationCallBackRefCout;
    s3eBool g_iPhoneHighRes;
    undefined field49_0xc1;
    undefined field50_0xc2;
    undefined field51_0xc3;
    double g_iPhoneScaleFactor;
    enum s3eDeviceOrientation g_OSOrientation;
    char g_TmpPath[256];
};

typedef enum s3eResult {
    S3E_RESULT_SUCCESS=0,
    S3E_RESULT_ERROR=1
} s3eResult;

typedef char * (*IwS3EEntryPoint)(s3eSymbolsInfo *);




undefined IwS3ERead(char * param_1, _func_int_void_ptr_int_void_ptr * param_2, void * param_3, uchar param_4);
s3eResult IwS3ECheckLicense(IwS3E *s3e);
IwS3EEntryPoint IwS3EGetEntryPoint(IwS3E *s3e);
void IwS3EDelete(IwS3E *s3e);
s3eResult IwS3EReadData(void *buffer,int size,IwS3E *s3e);
bool IwS3ESkip(IwS3E *s3e,int len);
s3eResult IwS3ESkipConfig(IwS3E *s3e);
s3eResult IwS3ELoadFixup(IwS3E *s3e);
s3eResult IwS3ELoadCode(IwS3E *s3e);
s3eResult IwS3ELoadSig(IwS3E *s3e);
s3eResult IwS3ELoadExtraSection(IwS3E *s3e);
char * IwS3EGetString(char *stringTab,int idx);
s3eResult IwS3EBuildHashtable(IwS3E *s3e);
void IwS3EFreeHashtable(IwS3E *s3e);
s3eResult IwS3EBuildHashList(IwS3E *s3e,IwS3ESymbolsSection *syms,uint32 *hashList);
int IwS3EGetSymbolFromHash(IwS3E *s3e,uint32 hash);
s3eResult IwS3EDoInternalRelocs(IwS3E *s3e,IwS3EInternalRelocSection *intrelocs);
s3eResult IwS3EDoExternalRelocs(IwS3E *s3e,IwS3EExternalRelocSection *extrelocs,uint32 *hashList,char *nameTable,bool bThumb,bool bAbs);
uint32 IwS3EGetRequiredVeneerSize(IwS3E *s3e);
undefined s3eUpdateSplash(void);
undefined s3eLoaderKeyIsActive(void);
undefined s3eGetDataLoadAddress(uint * param_1, uint * param_2);
undefined s3eLoaderKeyGetModulus(void);
undefined s3eLoaderKeyGetExponent(void);
undefined s3eSplashNotifyJuiceApp(void);
undefined IwS3EReadCheckLicenseData(IwS3EAdditionalData * param_1, int param_2);
undefined s3eLoaderKeyGetModulusLength(void);
undefined s3eLoaderKeyGetExponentLength(void);
undefined ___stack_chk_fail();

