	adc	r2 ,r11 ,r11
	vsub.d	d3 ,d31 ,d24
	vcge.f	q3 ,q11 ,q0
	str	r0 ,[r13]
	vaba.u32	q12 ,q11 ,q5
	adc	r9 ,r1 ,r4
	vadd.f	q3 ,q4 ,q15
	vbsl.f	q11 ,q8 ,q14
	vzip.8	q9 ,q0
	orr	r3 ,r11 ,r10
