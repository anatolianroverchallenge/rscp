// request_monitor.h
#ifndef REQUEST_MONITOR_H
#define REQUEST_MONITOR_H

#include <Arduino.h>
#include "rscp.pb.h"

/**
 * @brief Prints a GPS coordinate message.
 *
 * @param coord Pointer to the GPSCoordinate message.
 */
void print_GPSCoordinate(const rscp_GPSCoordinate *coord);

/**
 * @brief Prints the battery state message.
 *
 * @param battery Pointer to the BatteryState message.
 */
void print_BatteryState(const rscp_BatteryState *battery);

/**
 * @brief Prints the ArmDisarm message.
 *
 * @param msg Pointer to the ArmDisarm message.
 */
void print_ArmDisarm(const rscp_ArmDisarm *msg);

/**
 * @brief Prints the SetStage message.
 *
 * @param msg Pointer to the SetStage message.
 */
void print_SetStage(const rscp_SetStage *msg);

/**
 * @brief Prints the NavigateToGPS message.
 *
 * @param msg Pointer to the NavigateToGPS message.
 */
void print_NavigateToGPS(const rscp_NavigateToGPS *msg);

/**
 * @brief Prints the SearchArea message.
 *
 * @param msg Pointer to the SearchArea message.
 */
void print_SearchArea(const rscp_SearchArea *msg);

/**
 * @brief Dispatches printing based on the oneof field in RequestEnvelope.
 *
 * @param msg Pointer to the RequestEnvelope message.
 */
void print_RequestEnvelope(const rscp_RequestEnvelope *msg);

#endif // REQUEST_MONITOR_H
