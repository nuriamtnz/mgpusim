// memoryread_loop
__kernel void memoryread_loop(__global const float *in, 
                              __global float *out,
                              ulong stride, 
                              ulong vector_length) {

  __private unsigned long idx = get_global_id(0);

  for (; idx < vector_length; idx += stride) {
    out[idx] = in[idx];
  }
}