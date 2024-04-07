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
	and	r2 ,r3 ,r4
	mul	v5 ,v6 ,v7
	ldr r8, [r13]
	mov	r9 ,#94
	cmp	v4 ,v5
	add	v6 ,v7 ,v1
	mul	r4 ,r5, r6
	cmp	r9 ,r7
	add	v8 ,v3 ,v2
	str r10, [r13]

@ 0 "" 2
	.arm
	.syntax unified
	b	.L2
	.size	main, .-main
	.ident	"GCC: (Raspbian 10.2.1-6+rpi1) 10.2.1 20210110"
	.section	.note.GNU-stack,"",%progbits
