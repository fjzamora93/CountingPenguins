# Function to calculate normalized mae every pair of variables
nmae_function <- function(df, cols) {
  map_dfr(cols, function(pair) {
    col1 <- pair[1]
    col2 <- pair[2]
    
    if (col1 %in% names(df) && col2 %in% names(df)) {
      df %>%
        filter(!is.na(!!sym(col1)), !is.na(!!sym(col2))) %>%
        summarise(
          normalized_mae = sum(abs((!!sym(col2) - !!sym(col1)) / mean(!!sym(col1)))) / n()  # Calculate normalized bias
        ) %>%
        mutate(variable = paste(col1, "vs", col2))  # Add a label for the variable pair
    } else {
      data.frame(normalized_mae = NA, variable = paste(col1, "vs", col2))  # Return NA if columns are missing
    }
  })
}

# Define column pairs for calculation
cols_to_analyze <- list(
  c("temp_station", "temp_era5"),
  c("pres_station", "pres_era5"),
  c("vel_station", "vel_era5"),
  c("hr_station", "hr_era5")
)

# Calculate normalized biases for each data frame in combined_list
nmae_results_list <- map_dfr(names(combined_list), function(name) {
  df <- combined_list[[name]]
  nmae_results <- nmae_function(df, cols_to_analyze)
  nmae_results %>%
    mutate(station = name)  # Add station name to results
})

# Reshape the results into a wide format
wide_nmae_results <- nmae_results_list %>%
  pivot_wider(
    names_from = variable,
    values_from = normalized_mae
  )