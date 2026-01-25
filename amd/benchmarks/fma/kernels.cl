// memoryread_loop
__kernel void memoryread_loop(__global const float *in, 
                              __global float *out,
                              ulong stride, 
                              ulong vector_length,
                              float a, float b,
                              uint compute_iterations) {

  __private unsigned long idx = get_global_id(0);

  for (; idx < vector_length; idx += stride) {
    float x = in[idx];

    // Simulate some compute to increase temporal locality
    for (uint i = 0; i < compute_iterations; i++) {
      x = a * x + b;
    }

    out[idx] = x;
  }
}