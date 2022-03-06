e: If defrag was able to use acos math somehow, I'm guessing they found a mathematical alternative using other functions that generate equivalent output but I'm not a math expert
The reason for reimplementing complex math functions in qvm space is ill advised is due to the x87 fpu intermediate precision on real function calls is going to be more precise than on single precision floats only which you are restricted to inside qvm

f: I don't see why it would be ill advised, you can get as much precision as you need. it will be slower, that's all
if you need acos then you can get it, implement in bg_lib. maybe copy implementation from somewhere if you can.

e: Sure but it won't be double precision. Or rather 80bit

f: you wouldn't be able to consume it anyway, because in qvm you have only single precision floats available to you
you can implement acosf() or any other functions that will have 1 or less ULP precision using only 32bit floats and integers.
This means that result will be at most a single bit (least significant mantissa digit) different from exact result
expf() I linked earlier here has 1ULP accuracy
and in best scenario takes 11 multiplications, 11 additions and 11 divisions on floats. considering I wanted to use it twice a frame or so in cgame, it's nothing.
and it's certainly not state of the art algorithm, just something I wrote, while educating myself a bit on the internet
the problem with implementations from various libc you can find on the internet is that either they depend on double,
or use a ton of other math.h functions to implement what you want. or both. this is why I wrote my own (also for fun)

y: https://github.com/bradfa/musl/blob/master/src/math/acosf.c
musl impl is clean. GET_FLOAT_WORD and SET_FLOAT_WORD are all you need, which are int/float casts

f: needs sqrtf, but probably if you pull all dependencies it should be ok
y: doesn't qvm have that?
f: hm maybe it does, I don't remember
y: idk for sure but i thought it did. if not musl sqrtf doesn't have any dependencies
oh qvm only has sqrt for doubles
f: well, double is float in lcc. but it has low accuracy and you should make sure it doesn't make acosf() accuracy even worse.
may be best to copy sqrtf() from musl too then
y: yeah maybe
f: and sin() in bg_libc.c uses lookup table? if you don't need much accuracy you could do the same in reverse...
no but there is a syscall and this bg_lib.c sin() is removed with preprocessor. they are all in #if 0 block, together with this sqrt()...
y: yeah, sin syscall is available everywhere though. acos is only in cgame
