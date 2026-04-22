use std::time::Instant;

/// Linear congruential generator constants.
const A: u32 = 1103515245;
const C: u32 = 12345;

/// Compute the maximum subarray sum for an array of 100000 integers
/// The integers are uniformly distributed in the range [-10, 10].
fn max_subarray_sum(seed: u32) -> i128 {
    let mut state = seed;
    let range: u32 = 21;          // 10 - (-10) + 1
    let min_val: i32 = -10;

    let mut current: i128 = 0;
    // Use i128::MIN as the smallest possible value.
    let mut best: i128 = i128::MIN;

    for _ in 0..100_000u32 {
        // Generate the next random number.
        state = state.wrapping_mul(A).wrapping_add(C);
        let val: i32 = (state % range) as i32 + min_val;
        let val_i128: i128 = val as i128;

        current += val_i128;
        if current > best {
            best = current;
        }
        if current < 0 {
            current = 0;
        }
    }
    best
}

fn main() {
    let start_time = Instant::now();

    const MIN_SEED: u32 = 1;
    const MAX_SEED: u32 = 1000;

    let mut best_seed: u32 = 0;
    let mut best_sum: i128 = i128::MIN;

    for seed in MIN_SEED..=MAX_SEED {
        let sum = max_subarray_sum(seed);
        if best_seed == 0 || sum > best_sum {
            best_sum = sum;
            best_seed = seed;
        }
        println!("The sum of all subarray sums is {} for seed {}.", sum, seed);
    }
    println!("The best seed is {}.", best_seed);

    let elapsed = start_time.elapsed();
    eprintln!("Time elapsed: {:.3} secs", elapsed.as_secs_f64());
}