	.arch armv6
	.eabi_attribute 28, 1
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 6
	.eabi_attribute 34, 1
	.eabi_attribute 18, 4
	.file	"main.c"
	.text
	.align	2
	.global	main
	.arch armv6
	.syntax unified
	.arm
	.fpu vfp
	.type	main, %function
main:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
.L2:
	.syntax divided
@ 4 "main.c" 1
	mov r0, #10
    	mov r1, #5
    	add r2, r0, r1
    	sub r3, r0, r1
    	mul r4, r0, r1
    	cmp r0, r1
    	vadd.f64 d2, d0, d1
    	vsub.f64 d3, d0, d1
    	vmul.f64 d4, d0, d1
    	vcmp.f64 d0, d1
    	vcmpe.f64 d0, d1
    	vmrs r0, fpscr
	ldr  r5 ,[r13]
	str  r5 ,[r13]
        str  r12 ,[r13]


@ 0 "" 2
	.arm
	.syntax unified
	b	.L2
	.size	main, .-main
	.ident	"GCC: (Raspbian 10.2.1-6+rpi1) 10.2.1 20210110"
	.section	.note.GNU-stack,"",%progbits
