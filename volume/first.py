#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# NS-3 Python bindings example for 3 nodes:
# Node0 sends at 10 Mb/s, Node1 sends at 5 Mb/s, both to Node2

from ns import ns

def main():
    ns.LogComponentEnable("UdpClient", ns.LOG_LEVEL_INFO)
    ns.LogComponentEnable("UdpServer", ns.LOG_LEVEL_INFO)

    # 1. Create 3 nodes
    nodes = ns.NodeContainer()
    nodes.Create(3)

    # 2. Create point-to-point helper for Node0 <-> Node2
    p2p0 = ns.PointToPointHelper()
    p2p0.SetDeviceAttribute("DataRate", ns.StringValue("10Mbps"))
    p2p0.SetChannelAttribute("Delay", ns.StringValue("2ms"))

    # 3. Create point-to-point helper for Node1 <-> Node2
    p2p1 = ns.PointToPointHelper()
    p2p1.SetDeviceAttribute("DataRate", ns.StringValue("5Mbps"))
    p2p1.SetChannelAttribute("Delay", ns.StringValue("2ms"))

    # 4. Install devices on links
    ndc0 = ns.NetDeviceContainer()
    ndc0 = p2p0.Install(nodes.Get(0), nodes.Get(2))

    ndc1 = ns.NetDeviceContainer()
    ndc1 = p2p1.Install(nodes.Get(1), nodes.Get(2))

    # 5. Install Internet stack on all nodes
    stack = ns.InternetStackHelper()
    stack.Install(nodes)

    # 6. Assign IP addresses
    addr0 = ns.Ipv4AddressHelper()
    addr0.SetBase(ns.Ipv4Address("10.1.1.0"), ns.Ipv4Mask("255.255.255.0"))
    ip0 = addr0.Assign(ndc0)

    addr1 = ns.Ipv4AddressHelper()
    addr1.SetBase(ns.Ipv4Address("10.1.2.0"), ns.Ipv4Mask("255.255.255.0"))
    ip1 = addr1.Assign(ndc1)

    # 7. Create UDP server on Node2
    server_port = ns.UintegerValue(8080).Get()
    server = ns.UdpServerHelper(server_port)
    server_apps = server.Install(nodes.Get(2))
    server_apps.Start(ns.Seconds(1.0))
    server_apps.Stop(ns.Seconds(10.0))

    # 8. Create UDP clients on Node0 and Node1
    client0 = ns.UdpClientHelper(ip0.GetAddress(1).ConvertTo(), server_port)
    client0.SetAttribute("MaxPackets", ns.UintegerValue(1000))
    client0.SetAttribute("Interval", ns.TimeValue(ns.Seconds(0.01)))  # 10 Mb/s
    client0.SetAttribute("PacketSize", ns.UintegerValue(1024))

    client1 = ns.UdpClientHelper(ip1.GetAddress(1).ConvertTo(), server_port)
    client1.SetAttribute("MaxPackets", ns.UintegerValue(1000))
    client1.SetAttribute("Interval", ns.TimeValue(ns.Seconds(0.02)))  # 5 Mb/s
    client1.SetAttribute("PacketSize", ns.UintegerValue(1024))

    client_apps0 = client0.Install(nodes.Get(0))
    client_apps0.Start(ns.Seconds(2.0))
    client_apps0.Stop(ns.Seconds(10.0))

    client_apps1 = client1.Install(nodes.Get(1))
    client_apps1.Start(ns.Seconds(2.0))
    client_apps1.Stop(ns.Seconds(10.0))

    # 9. Enable pcap tracing (optional, generates .pcap files)
    p2p0.EnablePcapAll("node0_node2")
    p2p1.EnablePcapAll("node1_node2")

    # 10. Run the simulation
    ns.Simulator.Run()
    ns.Simulator.Destroy()

if __name__ == "__main__":
    main()

