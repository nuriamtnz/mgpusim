// vectorRead
__kernel void vectorRead(__global const float* in, 
                         __global float* out) {
  __private int index = get_global_id(0);
  out[index] = in[index];
}