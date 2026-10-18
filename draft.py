from models import TicketInfo, Ticket


tickets_info = [[1000001, "VPN", "This a tests for employee 1000001"], [1000002, "Network", "This a test for employee 1000002"]]

tickets_list =[]
for info in tickets_info:
    for i in info:
        print(i)