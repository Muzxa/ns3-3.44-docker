#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ns import ns

def main():
    # Enable logging
    ns.LogComponentEnable("UdpClient", ns.LOG_LEVEL_INFO)
    ns.LogComponentEnable("UdpServer", ns.LOG_LEVEL_INFO)

    # 1. Create nodes
    nodes = ns.NodeContainer()
    nodes.Create(3)

    # 2. Set up Wi-Fi channel & PHY
    phy = ns.YansWifiPhyHelper()
    channel = ns.YansWifiChannelHelper()
    channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
    channel.AddPropagationLoss("ns3::FriisPropagationLossModel")
    phy.SetChannel(channel.Create())

    # 3. Wi-Fi helper
    wifi = ns.WifiHelper()
    wifi.SetStandard("802.11g")  # use string here, not enum

    mac = ns.WifiMacHelper()
    mac.SetType("ns3::StaWifiMac", "Ssid", ns.SsidValue(ns.Ssid("wifi-ssid")))
    staDevices = wifi.Install(phy, mac, nodes.Get(1))  # node-1 sender

    mac.SetType("ns3::ApWifiMac", "Ssid", ns.SsidValue(ns.Ssid("wifi-ssid")))
    apDevices = wifi.Install(phy, mac, nodes.Get(2))   # node-2 receiver

    # 4. Mobility
    mobility = ns.MobilityHelper()
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobility.Install(nodes)

    # 5. Internet stack
    stack = ns.InternetStackHelper()
    stack.Install(nodes)

    # 6. Assign IP addresses
    address = ns.Ipv4AddressHelper()
    address.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))
    interfaces = address.Assign(ns.NetDeviceContainer(staDevices, apDevices))

    # 7. UDP server on node-2
    server_port = 8080
    server = ns.UdpServerHelper(server_port)
    serverApps = server.Install(nodes.Get(2))
    serverApps.Start(ns.Seconds(1.0))
    serverApps.Stop(ns.Seconds(10.0))

    # 8. UDP client on node-1
    client = ns.UdpClientHelper(interfaces.GetAddress(1).ConvertTo(), server_port)
    client.SetAttribute("MaxPackets", ns.UintegerValue(1000))
    client.SetAttribute("Interval", ns.TimeValue(ns.Seconds(0.02)))  # 5 Mb/s
    client.SetAttribute("PacketSize", ns.UintegerValue(1024))

    clientApps = client.Install(nodes.Get(1))
    clientApps.Start(ns.Seconds(2.0))
    clientApps.Stop(ns.Seconds(10.0))

    # 9. Enable pcap tracing
    phy.EnablePcapAll("node1_node2_wireless")

    # 10. Run simulation
    ns.Simulator.Stop(ns.Seconds(5.0))
    ns.Simulator.Run()
    ns.Simulator.Destroy()

if __name__ == "__main__":
    main()
