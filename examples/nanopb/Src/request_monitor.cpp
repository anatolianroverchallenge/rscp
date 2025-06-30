// request_monitor.cpp
#include "request_monitor.h"

void print_GPSCoordinate(const rscp_GPSCoordinate *coord)
{
    Serial.println("GPSCoordinate {");
    Serial.print("  latitude: ");
    Serial.println(coord->latitude, 6);
    Serial.print("  longitude: ");
    Serial.println(coord->longitude, 6);
    Serial.print("  altitude: ");
    Serial.println(coord->altitude, 3);
    Serial.println("}");
}

void print_BatteryState(const rscp_BatteryState *battery)
{
    Serial.println("BatteryState {");
    Serial.print("  voltage: ");
    Serial.println(battery->voltage, 3);
    Serial.print("  current: ");
    Serial.println(battery->current, 3);
    Serial.print("  state_of_charge: ");
    Serial.println(battery->state_of_charge, 3);
    Serial.println("}");
}

void print_ArmDisarm(const rscp_ArmDisarm *msg)
{
    Serial.print("ArmDisarm { value: ");
    Serial.print(msg->value ? "true" : "false");
    Serial.println(" }");
}

void print_SetStage(const rscp_SetStage *msg)
{
    Serial.print("SetStage { value: ");
    Serial.print(msg->value);
    Serial.println(" }");
}

void print_NavigateToGPS(const rscp_NavigateToGPS *msg)
{
    Serial.println("NavigateToGPS {");
    print_GPSCoordinate(&msg->coordinate);
    Serial.println("}");
}

void print_SearchArea(const rscp_SearchArea *msg)
{
    Serial.println("SearchArea {");
    print_GPSCoordinate(&msg->center_coordinate);
    Serial.print("  radius: ");
    Serial.println(msg->radius, 3);
    Serial.println("}");
}

void print_start_exploration(const rscp_StartExploration *msg)
{
    Serial.println("Start Exploration {}");

}

void print_RequestEnvelope(const rscp_RequestEnvelope *msg)
{
    if (!msg)
    {
        Serial.println("Null message pointer");
        return;
    }
    Serial.print("Received Request type: ");
    Serial.println(msg->which_request);
    switch (msg->which_request)
    {
    case rscp_RequestEnvelope_arm_disarm_tag:
        print_ArmDisarm(&msg->request.arm_disarm);
        break;
    case rscp_RequestEnvelope_set_stage_tag:
        print_SetStage(&msg->request.set_stage);
        break;
    case rscp_RequestEnvelope_navigate_to_gps_tag:
        print_NavigateToGPS(&msg->request.navigate_to_gps);
        break;
    case rscp_RequestEnvelope_search_area_tag:
        print_SearchArea(&msg->request.search_area);
        break;
    case rscp_RequestEnvelope_start_exploration_tag:
        print_start_exploration(&msg->request.start_exploration);
        break;
    default:
        Serial.println("Unknown request type");
        break;
    }
}
