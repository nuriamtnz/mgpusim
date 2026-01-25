	.text
	.hsa_code_object_version 2,1
	.hsa_code_object_isa 8,0,3,"AMD","AMDGPU"
	.protected	memoryread_loop ; -- Begin function memoryread_loop
	.globl	memoryread_loop
	.p2align	8
	.type	memoryread_loop,@function
	.amdgpu_hsa_kernel memoryread_loop
memoryread_loop:                        ; @memoryread_loop
memoryread_loop$local:
	.amd_kernel_code_t
		amd_code_version_major = 1
		amd_code_version_minor = 2
		amd_machine_kind = 1
		amd_machine_version_major = 8
		amd_machine_version_minor = 0
		amd_machine_version_stepping = 3
		kernel_code_entry_byte_offset = 256
		kernel_code_prefetch_byte_size = 0
		granulated_workitem_vgpr_count = 2
		granulated_wavefront_sgpr_count = 2
		priority = 0
		float_mode = 192
		priv = 0
		enable_dx10_clamp = 1
		debug_mode = 0
		enable_ieee_mode = 1
		enable_wgp_mode = 0
		enable_mem_ordered = 0
		enable_fwd_progress = 0
		enable_sgpr_private_segment_wave_byte_offset = 0
		user_sgpr_count = 8
		enable_trap_handler = 0
		enable_sgpr_workgroup_id_x = 1
		enable_sgpr_workgroup_id_y = 0
		enable_sgpr_workgroup_id_z = 0
		enable_sgpr_workgroup_info = 0
		enable_vgpr_workitem_id = 0
		enable_exception_msb = 0
		granulated_lds_size = 0
		enable_exception = 0
		enable_sgpr_private_segment_buffer = 1
		enable_sgpr_dispatch_ptr = 1
		enable_sgpr_queue_ptr = 0
		enable_sgpr_kernarg_segment_ptr = 1
		enable_sgpr_dispatch_id = 0
		enable_sgpr_flat_scratch_init = 0
		enable_sgpr_private_segment_size = 0
		enable_sgpr_grid_workgroup_count_x = 0
		enable_sgpr_grid_workgroup_count_y = 0
		enable_sgpr_grid_workgroup_count_z = 0
		enable_wavefront_size32 = 0
		enable_ordered_append_gds = 0
		private_element_size = 1
		is_ptr64 = 1
		is_dynamic_callstack = 0
		is_debug_enabled = 0
		is_xnack_enabled = 0
		workitem_private_segment_byte_size = 0
		workgroup_group_segment_byte_size = 0
		gds_segment_byte_size = 0
		kernarg_segment_byte_size = 104
		workgroup_fbarrier_count = 0
		wavefront_sgpr_count = 22
		workitem_vgpr_count = 10
		reserved_vgpr_first = 0
		reserved_vgpr_count = 0
		reserved_sgpr_first = 0
		reserved_sgpr_count = 0
		debug_wavefront_private_segment_offset_sgpr = 0
		debug_private_segment_buffer_sgpr = 0
		kernarg_segment_alignment = 4
		group_segment_alignment = 4
		private_segment_alignment = 4
		wavefront_size = 6
		call_convention = -1
		runtime_loader_kernel_symbol = 0
	.end_amd_kernel_code_t
; %bb.0:
	s_load_dwordx8 s[12:19], s[6:7], 0x0
	s_load_dwordx2 s[0:1], s[6:7], 0x30
	s_load_dword s2, s[4:5], 0x4
	s_waitcnt lgkmcnt(0)
	v_mov_b32_e32 v1, s1
	s_and_b32 s2, s2, 0xffff
	s_mul_i32 s8, s8, s2
	v_add_u32_e32 v0, vcc, s8, v0
	v_add_u32_e32 v0, vcc, s0, v0
	v_addc_u32_e32 v1, vcc, 0, v1, vcc
	v_cmp_gt_u64_e32 vcc, s[18:19], v[0:1]
	s_and_saveexec_b64 s[0:1], vcc
	s_cbranch_execz BB0_10
; %bb.1:
	s_load_dwordx4 s[4:7], s[6:7], 0x20
	s_mov_b64 s[0:1], -1
	s_waitcnt lgkmcnt(0)
	s_cmp_eq_u32 s6, 0
	s_cbranch_scc1 BB0_7
; %bb.2:                                ; %.preheader3.preheader
	v_mov_b32_e32 v3, v1
	s_mov_b64 s[2:3], 0
	v_mov_b32_e32 v2, v0
BB0_3:                                  ; %.preheader3
                                        ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB0_4 Depth 2
	v_lshlrev_b64 v[4:5], 2, v[2:3]
	v_mov_b32_e32 v6, s13
	v_add_u32_e32 v4, vcc, s12, v4
	v_addc_u32_e32 v5, vcc, v6, v5, vcc
	flat_load_dword v4, v[4:5]
	s_mov_b32 s0, s6
BB0_4:                                  ;   Parent Loop BB0_3 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	s_add_i32 s0, s0, -1
	v_mov_b32_e32 v5, s5
	s_cmp_lg_u32 s0, 0
	s_waitcnt vmcnt(0) lgkmcnt(0)
	v_mad_f32 v4, s4, v4, v5
	s_cbranch_scc1 BB0_4
; %bb.5:                                ;   in Loop: Header=BB0_3 Depth=1
	v_lshlrev_b64 v[5:6], 2, v[2:3]
	v_mov_b32_e32 v8, s17
	v_add_u32_e32 v2, vcc, s16, v2
	v_addc_u32_e32 v3, vcc, v3, v8, vcc
	v_cmp_le_u64_e32 vcc, s[18:19], v[2:3]
	v_mov_b32_e32 v7, s15
	v_add_u32_e64 v5, s[0:1], s14, v5
	v_addc_u32_e64 v6, s[0:1], v7, v6, s[0:1]
	s_or_b64 s[2:3], vcc, s[2:3]
	flat_store_dword v[5:6], v4
	s_andn2_b64 exec, exec, s[2:3]
	s_cbranch_execnz BB0_3
; %bb.6:                                ; %Flow
	s_or_b64 exec, exec, s[2:3]
	s_mov_b64 s[0:1], 0
BB0_7:                                  ; %Flow36
	s_and_b64 vcc, exec, s[0:1]
	s_cbranch_vccz BB0_10
; %bb.8:                                ; %.preheader.preheader
	v_lshlrev_b64 v[2:3], 2, v[0:1]
	s_lshl_b64 s[4:5], s[16:17], 2
	s_mov_b64 s[6:7], 0
BB0_9:                                  ; %.preheader
                                        ; =>This Inner Loop Header: Depth=1
	v_mov_b32_e32 v5, s13
	v_add_u32_e64 v6, s[0:1], s12, v2
	v_addc_u32_e64 v7, s[0:1], v5, v3, s[0:1]
	flat_load_dword v6, v[6:7]
	v_add_u32_e32 v4, vcc, s14, v2
	v_mov_b32_e32 v8, s15
	v_mov_b32_e32 v9, s5
	v_add_u32_e64 v2, s[2:3], s4, v2
	v_addc_u32_e32 v5, vcc, v8, v3, vcc
	v_addc_u32_e64 v3, vcc, v3, v9, s[2:3]
	v_mov_b32_e32 v7, s17
	v_add_u32_e32 v0, vcc, s16, v0
	v_addc_u32_e32 v1, vcc, v1, v7, vcc
	v_cmp_le_u64_e32 vcc, s[18:19], v[0:1]
	s_or_b64 s[6:7], vcc, s[6:7]
	s_waitcnt vmcnt(0) lgkmcnt(0)
	flat_store_dword v[4:5], v6
	s_andn2_b64 exec, exec, s[6:7]
	s_cbranch_execnz BB0_9
BB0_10:                                 ; %.loopexit
	s_endpgm
.Lfunc_end0:
	.size	memoryread_loop, .Lfunc_end0-memoryread_loop
                                        ; -- End function
	.section	.AMDGPU.csdata
; Kernel info:
; codeLenInByte = 364
; NumSgprs: 22
; NumVgprs: 10
; ScratchSize: 0
; MemoryBound: 0
; FloatMode: 192
; IeeeMode: 1
; LDSByteSize: 0 bytes/workgroup (compile time only)
; SGPRBlocks: 2
; VGPRBlocks: 2
; NumSGPRsForWavesPerEU: 22
; NumVGPRsForWavesPerEU: 10
; Occupancy: 10
; WaveLimiterHint : 1
; COMPUTE_PGM_RSRC2:USER_SGPR: 8
; COMPUTE_PGM_RSRC2:TRAP_HANDLER: 0
; COMPUTE_PGM_RSRC2:TGID_X_EN: 1
; COMPUTE_PGM_RSRC2:TGID_Y_EN: 0
; COMPUTE_PGM_RSRC2:TGID_Z_EN: 0
; COMPUTE_PGM_RSRC2:TIDIG_COMP_CNT: 0
	.ident	"clang version 11.0.0 (/src/external/llvm-project/clang b98349b12ffa706d0e863a3f1176b20d2a6c438b)"
	.section	".note.GNU-stack"
	.addrsig
	.amd_amdgpu_isa "amdgcn-amd-amdhsa--gfx803"
	.amd_amdgpu_hsa_metadata
---
Version:         [ 1, 0 ]
Kernels:
  - Name:            memoryread_loop
    SymbolName:      'memoryread_loop@kd'
    Language:        OpenCL C
    LanguageVersion: [ 1, 2 ]
    Args:
      - Name:            in
        TypeName:        'float*'
        Size:            8
        Align:           8
        ValueKind:       GlobalBuffer
        ValueType:       F32
        AddrSpaceQual:   Global
        AccQual:         Default
        IsConst:         true
      - Name:            out
        TypeName:        'float*'
        Size:            8
        Align:           8
        ValueKind:       GlobalBuffer
        ValueType:       F32
        AddrSpaceQual:   Global
        AccQual:         Default
      - Name:            stride
        TypeName:        ulong
        Size:            8
        Align:           8
        ValueKind:       ByValue
        ValueType:       U64
        AccQual:         Default
      - Name:            vector_length
        TypeName:        ulong
        Size:            8
        Align:           8
        ValueKind:       ByValue
        ValueType:       U64
        AccQual:         Default
      - Name:            a
        TypeName:        float
        Size:            4
        Align:           4
        ValueKind:       ByValue
        ValueType:       F32
        AccQual:         Default
      - Name:            b
        TypeName:        float
        Size:            4
        Align:           4
        ValueKind:       ByValue
        ValueType:       F32
        AccQual:         Default
      - Name:            compute_iterations
        TypeName:        uint
        Size:            4
        Align:           4
        ValueKind:       ByValue
        ValueType:       U32
        AccQual:         Default
      - Size:            8
        Align:           8
        ValueKind:       HiddenGlobalOffsetX
        ValueType:       I64
      - Size:            8
        Align:           8
        ValueKind:       HiddenGlobalOffsetY
        ValueType:       I64
      - Size:            8
        Align:           8
        ValueKind:       HiddenGlobalOffsetZ
        ValueType:       I64
      - Size:            8
        Align:           8
        ValueKind:       HiddenNone
        ValueType:       I8
        AddrSpaceQual:   Global
      - Size:            8
        Align:           8
        ValueKind:       HiddenNone
        ValueType:       I8
        AddrSpaceQual:   Global
      - Size:            8
        Align:           8
        ValueKind:       HiddenNone
        ValueType:       I8
        AddrSpaceQual:   Global
      - Size:            8
        Align:           8
        ValueKind:       HiddenMultiGridSyncArg
        ValueType:       I8
        AddrSpaceQual:   Global
    CodeProps:
      KernargSegmentSize: 104
      GroupSegmentFixedSize: 0
      PrivateSegmentFixedSize: 0
      KernargSegmentAlign: 8
      WavefrontSize:   64
      NumSGPRs:        22
      NumVGPRs:        10
      MaxFlatWorkGroupSize: 256
...

	.end_amd_amdgpu_hsa_metadata
