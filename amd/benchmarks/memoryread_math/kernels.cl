// vectorRead
__kernel void vectorRead(__global const float* in, 
                         __global float* out) {
  __private int index = get_global_id(0);

  __private float in_value;
  
  in_value = in[index];
  in_value = in_value * 2.0f;
  out[index] = in_value;
}