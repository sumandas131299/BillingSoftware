class TemplateList():
    def __init__(self):
        list=[]
    
    def allTemplateList():
        template1 = html_content = """
                <html>
                <head>
                    <title>Tax Invoice</title>
                    <style>
                        @media print {{
                            body, .container {{
                                width: 793px;
                                height: 2500px;
                                margin: 0;
                                padding: 0;
                                page-break-before: always;
                            }}
                            .container {{
                                border: 1px solid #000;
                                padding: 20px;
                                box-sizing: border-box;
                                display: flex;
                                flex-direction: column;
                                justify-content: space-between;
                            }}
                        }}
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #fff;
                        }}
                        .container {{
                            width: 893px;
                            height: auto;
                            margin: 0 auto;
                            padding: 20px;
                            border: 1px solid #000;
                            box-sizing: border-box;
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                            page-break-after: always;
                        }}
                        .header, .footer {{
                            text-align: center;
                        }}
                        .header h1 {{
                            background-color: #d3aefc;
                            padding: 10px;
                            font-size: 24px;
                        }}
                        .items th {{
                            background-color: {selected_color};
                        }}
                        .items, .summary, .installments {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        .items th, .items td, .summary td, .installments td {{
                            border: 1px solid #000;
                            padding: 8px;
                        }}
                        .items .description {{
                            text-align: left;
                        }}
                        .summary {{
                            margin-left: 60%;
                        }}
                        .summary td {{
                            text-align: right;
                            padding-right: 68px;
                        }}
                        .summary .label {{
                            text-align: left;
                        }}
                        .Signature {{
                            text-align: right;
                            font-weight: bold;
                        }}
                        
                        .footer {{
                            margin-top: 20px;
                            text-align: center;
                            font-size: 15px;
                        }}
                        .fix {{
                            height: 350px;
                            width: 100%;
                            display: flex;
                        }}
                    </style>
                </head>
                <body>
                """
                # Replace `{selected_color}` with the actual color value
        html_content = html_content.format(selected_color=selected_color)

            # Splitting services into pages of 8 items each
        for page_number, start_idx in enumerate(range(0, len(selected_services), 8)):
                    page_services = selected_services[start_idx:start_idx + 8]

                    html_content += f"""
                    <div class="container" style="position:relative">
                        <table class="header-table" style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="border: none;">
                                    <strong>Company/Seller Name: Geek Thrive</strong><br>
                                    Address: 23 GORA CHAND ROAD KOL-14<br>
                                    Phone No.: 6291843612<br>
                                    Email ID: support@geekthrive.com<br>
                                </td>
                                <td style="border: none; position: absolute; left: 46%; top: 2%; ">
                                    <img src="{logo_path}" alt="Company Logo" style="height: 80px;">
                                </td>
                                <td style="border: none; text-align: right;">
                                    <img src="{scanner_path}" alt="Company Logo" style="height: 80px;">
                                </td>
                            </tr>
                        </table>
                        <br>
                        <h1 style="text-align: center">{"Tax Invoice" if gst_applicable else "Invoice"}</h1><br>
                        <table class="details" style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td>
                                    <strong>Billed To:</strong><br>
                                    Name: {name} <br>
                                    Address: {address}<br>
                                    Contact No.: {contact_number}<br>
                                </td>
                                <td>
                                    <strong>Shipping To:</strong><br>
                                    Name: {name}<br>
                                    Address: {address}<br>
                                    Contact No.: {contact_number}
                                </td>
                                <td>
                                    <strong>Invoice No.:</strong> {invoice_number}<br>
                                    <strong>Date:</strong> {current_date}
                                </td>
                            </tr>
                        </table>
                        <br>
                        <div class = "fix">
                        <table class="items" style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <th style="width: 5%;">Sl</th>
                                <th style="width: 25%;">Item Name</th>
                                <th style="width: 30%;">Description</th>
                                <th style="width: 10%;">Rate</th>
                                <th style="width: 15%;">Discount</th>
                                <th style="width: 15%;">Amount</th>
                            </tr>
                    """

                    
                    item=0
                    # Adding each service for this page
                    sl_number = 1  # Start serial number from 1
                    for service_info in self.services_info:
                        item+=1
                        if service_info["discount_percentage"] > 0:
                            html_content += f"""
                                <tr style="text-align: center">
                                    <td>{sl_number}</td>  <!-- Sl (Serial Number) -->
                                    <td>{service_info["service"] or ""}</td>  <!-- Item Name (service) -->
                                    <td>{service_info["plan"]or ""} ({service_info["discount_percentage"]or ""}% discount)</td>     <!-- Description (plan) -->
                                    <td>&#8377;{service_info["base_price"]or ""}</td> <!-- Rate (base_price) -->
                                    <td>&#8377;{service_info["discount_amount"] or 0:.2f}</td> <!-- Discount (discount_amount) -->
                                    <td>&#8377;{service_info["discounted_price"] or 0:.2f}</td> <!-- Amount (discounted_price) -->            
                                </tr>
                            """
                        else:  # No discount
                            html_content += f"""
                                <tr style="text-align: center">
                                    <td>{sl_number}</td>  <!-- Sl (Serial Number) -->
                                    <td>{service_info["service"]}</td>  <!-- Item Name (service) -->
                                    <td>{service_info["plan"]}</td>     <!-- Description (plan) -->
                                    <td>&#8377;{service_info["base_price"]}</td> <!-- Rate (base_price) -->
                                    <td>&#8377;</td> <!-- Discount (no discount) -->
                                    <td>&#8377;{service_info["discounted_price"]:.2f}</td> <!-- Amount (discounted_price) -->
                                </tr>
                            """
                        sl_number += 1  # Increment serial number for next service

                    switch_dict = {
                        8: 7,
                        7: 9,
                        6: 11,
                        5: 13,
                        4: 15,
                        3: 17,
                        2: 19,
                        1: 21,
                        9: 7,
                        10: 9,
                        11: 11,
                        12: 13,
                        13: 15,
                        14: 17,
                        15: 19,
                        16: 21,
                        17: 7,
                        18: 9,
                        19: 11,
                        20: 13,
                        21: 15,
                        22: 17,
                        23: 19,
                        24: 21
                    }
                    loopBr = switch_dict.get(item)
                    print(loopBr)
                    # Adding installments table
                    html_content += """
                        <table class="installments" style="width: 55%; border-collapse: collapse; border: 1px solid black;">
                            <tr>
                                <th style="width: 25%;">Installment Description</th>
                            </tr>
                        
                        
                    """
                    if isinstance(loopBr, int) and loopBr > 0:
                        html_content+=f'{"<br>" * loopBr}'
                
                    

                    # Initialize an empty list to hold all installment descriptions
                    installments = []

                    # Loop through the installments list
                    for i in range(self.installment_list.count()):
                        item_text = self.installment_list.item(i).text()
                        
                        if amount:
                            # Remove the ₹ symbol from the installment description
                            item_text_without_ruppee = item_text.replace("₹", "").strip()
                            
                            # Add the cleaned-up installment to the list
                            installments.append(item_text_without_ruppee)

                    # Join all installments into a single string, separated by semicolons
                    installments_str = " ; ".join(installments)

                    # Add the combined string to a single table cell
                    html_content += f"""
                    <tr>
                        <td>{installments_str or ""}</td>
                    </tr>
                    <tr>
                                <td><strong>Total : {total_installments or ""}/-</strong></td>
                            </tr>
                    
                    """

                    html_content += "</table>"


                    # Adding the summary to each page


                    

                    html_content += f"""
                        </table>
                        </div>
                        """
                        
                    if not gst_applicable :
                        print(gst_applicable )
                        html_content += f"""
                        <br><br><br>
                        <br><br>
                        
                        """
                        
                    html_content += f"""
                        <br><br><br>
                        <table class="summary" style=" display: inline; width: 40%; border-collapse: collapse;">
                            <tr><td class="label"><strong>Total:</strong></td><td><strong>{self.total_discounted_price or 0  }</strong></td></tr>
                            {(f'<tr><td class="label">SGST:</td><td>{sgst_amount or 0:.2f  }</td></tr>' if gst_applicable else '')}
                            {(f'<tr><td class="label">CGST:</td><td>{cgst_amount or 0:.2f  }</td></tr>' if gst_applicable else '')}
                            <tr><td class="label">Received:</td><td>{total_receive or 0 }</td></tr>
                            <tr><td class="label">Balance:</td><td>{balance or 0  }</td></tr>
                            <tr><td class="label"><strong>Grand Total:</strong></td><td><strong>&#8377;{round(balance) or "" }/-</strong></td></tr>
                        </table>
                        <br><br>
                        <br>
                        <p><strong>Amount in words:</strong> {total_amount_in_words or "" } rupees only</p>
                        <div class="Signature">
                            <p>For <strong>Geek Thrive</strong></p>
                            <img src="{signature_path}" alt="Signature" style="height: 60px;">
                            <p>Authorized Signature</p>
                        </div>
                        <div class="footer">
                            <br>
                            <p>Thank you for choosing Geek Thrive for your business. All payments must be completed before the final delivery of the product.</p>
                            </div>
                        </div>
                    </div>
                    """
        html_content += "</body></html>"


        list.append(template1)

        print(template1)
if __name__ == "__main__":
    
    print(TemplateList.list)