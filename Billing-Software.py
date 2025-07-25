from tkinter import *
from tkinter import ttk, messagebox
from fpdf import FPDF
import os
from datetime import datetime
import webbrowser

# Configuration
BILLS_FOLDER = "Suprate"
if not os.path.exists(BILLS_FOLDER):
    os.makedirs(BILLS_FOLDER)

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'TAX INVOICE CUM DC', ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, 'SHANTHI ENTERPRISES\nPritchard Rd, M.G.Market, Robertson pet, K G F, Kolar Dist\nM: 9900956272 | PH: - | GSTIN: 29BZUPM0198R1Z1', align='C')
        self.ln(5)

    def add_buyer_details(self, name, phone, bill_no):
        self.set_font('Helvetica', '', 10)
        self.cell(100, 6, f"Buyer: {name}", ln=0)
        self.cell(0, 6, f"Bill Date: {datetime.now().strftime('%d-%m-%Y')}", ln=1)
        self.cell(100, 6, f"KGF - M: {phone}", ln=0)
        self.cell(0, 6, f"Bill No: {bill_no}", ln=1)
        self.cell(100, 6, "GSTIN of Buyer: ", ln=0)
        self.cell(0, 6, "Sales Man: MADHU", ln=1)
        self.cell(100, 6, "Route: CREDIT/DEBIT", ln=0)
        self.cell(0, 6, "Work Order No: ", ln=1)
        self.cell(100, 6, "PAN: ", ln=0)
        self.cell(0, 6, "Work Order Type: ", ln=1)
        self.cell(100, 6, "Delivery At: ", ln=0)
        self.cell(0, 6, f"Purchase Order Date: {datetime.now().strftime('%d-%m-%Y')}", ln=1)
        self.ln(5)

    def add_item_table(self, product, hsn, imei, qty, rate, tax_percent, discount_percent=0):
        subtotal = float(rate) * int(qty)
        discount_amount = subtotal * discount_percent / 100
        taxable_amount = subtotal - discount_amount
        tax_amt = taxable_amount * tax_percent / 100
        total = taxable_amount + tax_amt

        self.set_font('Helvetica', 'B', 10)
        self.cell(10, 6, "#", 1)
        self.cell(45, 6, "Product", 1)
        self.cell(25, 6, "HSN", 1)
        self.cell(40, 6, "IMEI", 1)
        self.cell(15, 6, "Qty", 1)
        self.cell(25, 6, "Rate", 1)
        self.cell(15, 6, "Tax%", 1)
        self.cell(0, 6, "Total", 1, ln=1)

        self.set_font('Helvetica', '', 10)
        self.cell(10, 6, "1", 1)
        self.cell(45, 6, product[:20], 1)
        self.cell(25, 6, hsn, 1)
        self.cell(40, 6, imei[:20], 1)
        self.cell(15, 6, str(qty), 1)
        self.cell(25, 6, f"{float(rate):.2f}", 1)
        self.cell(15, 6, f"{tax_percent}%", 1)
        self.cell(0, 6, f"{total:.2f}", 1, ln=1)

        self.ln(5)
        if discount_percent > 0:
            self.cell(0, 6, f"Subtotal: Rs. {subtotal:.2f}", ln=1)
            self.cell(0, 6, f"Discount ({discount_percent}%): Rs. {discount_amount:.2f}", ln=1)
            self.cell(0, 6, f"Taxable Amount: Rs. {taxable_amount:.2f}", ln=1)
        self.cell(0, 6, f"CGST 9%: Rs. {tax_amt/2:.2f}", ln=1)
        self.cell(0, 6, f"SGST 9%: Rs. {tax_amt/2:.2f}", ln=1)
        self.cell(0, 6, f"Net Amount: Rs. {total:.2f}", ln=1)

    def add_footer(self):
        self.ln(10)
        self.set_font('Helvetica', 'I', 9)
        self.multi_cell(0, 5, "Terms & Conditions:\nGoods once sold cannot be taken back or exchanged.\nFor service issues, contact the nearest service center.", align='L')
        self.cell(0, 6, "For SHANTHI ENTERPRISES", ln=True, align='R')
        self.cell(0, 6, "Authorized Signatory", ln=True, align='R')

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Invoice Generator - Shanthi Enterprises")
        self.root.geometry("800x600")
        self.bill_counter = 1
        
        # Create styles
        self.create_styles()
        
        # Build UI
        self.build_ui()
        
    def create_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Error.TLabel', foreground='red')
        
    def build_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Invoice Generator", style='Header.TLabel')
        title_label.pack(pady=(0, 15))
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=BOTH, expand=True)
        
        # Invoice Tab
        invoice_tab = ttk.Frame(notebook)
        notebook.add(invoice_tab, text="Create Invoice")
        
        # Customer Frame
        customer_frame = ttk.LabelFrame(invoice_tab, text="Customer Details", padding=10)
        customer_frame.pack(fill=X, padx=5, pady=5)
        
        ttk.Label(customer_frame, text="Name*:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_name = ttk.Entry(customer_frame, width=40)
        self.entry_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(customer_frame, text="Phone*:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_phone = ttk.Entry(customer_frame, width=40)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(customer_frame, text="Delivery At:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_delivery = ttk.Entry(customer_frame, width=40)
        self.entry_delivery.grid(row=2, column=1, padx=5, pady=2)
        
        # Product Frame
        product_frame = ttk.LabelFrame(invoice_tab, text="Product Details", padding=10)
        product_frame.pack(fill=X, padx=5, pady=5)
        
        ttk.Label(product_frame, text="Product Name*:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_product = ttk.Entry(product_frame, width=40)
        self.entry_product.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(product_frame, text="HSN Code*:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_hsn = ttk.Entry(product_frame, width=40)
        self.entry_hsn.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(product_frame, text="IMEI Number*:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_imei = ttk.Entry(product_frame, width=40)
        self.entry_imei.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(product_frame, text="Quantity*:").grid(row=3, column=0, sticky=W, pady=2)
        self.entry_qty = ttk.Entry(product_frame, width=40)
        self.entry_qty.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(product_frame, text="Rate (Rs)*:").grid(row=4, column=0, sticky=W, pady=2)
        self.entry_rate = ttk.Entry(product_frame, width=40)
        self.entry_rate.grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(product_frame, text="Discount (%):").grid(row=5, column=0, sticky=W, pady=2)
        self.entry_discount = ttk.Entry(product_frame, width=40)
        self.entry_discount.insert(0, "0")
        self.entry_discount.grid(row=5, column=1, padx=5, pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(invoice_tab)
        button_frame.pack(fill=X, pady=10)
        
        generate_btn = ttk.Button(button_frame, text="Generate Invoice", command=self.generate_invoice)
        generate_btn.pack(side=LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        clear_btn.pack(side=LEFT, padx=5)
        
        # Settings Tab
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Settings")
        
        settings_frame = ttk.LabelFrame(settings_tab, text="Company Settings", padding=10)
        settings_frame.pack(fill=BOTH, padx=10, pady=10)
        
        ttk.Label(settings_frame, text="Next Bill Number:").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_bill_counter = ttk.Entry(settings_frame, width=40)
        self.entry_bill_counter.insert(0, str(self.bill_counter))
        self.entry_bill_counter.grid(row=0, column=1, padx=5, pady=5)
        
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
        
    def generate_invoice(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        product = self.entry_product.get().strip()
        hsn = self.entry_hsn.get().strip()
        imei = self.entry_imei.get().strip()
        qty = self.entry_qty.get().strip()
        rate = self.entry_rate.get().strip()
        discount = self.entry_discount.get().strip() or "0"
        delivery_at = self.entry_delivery.get().strip()

        if not all([name, phone, product, hsn, imei, qty, rate]):
            messagebox.showerror("Missing Info", "Please fill all required fields.")
            return

        try:
            qty = int(qty)
            rate = float(rate)
            discount = float(discount)
            if discount < 0 or discount > 100:
                raise ValueError("Discount must be between 0 and 100")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input:\n- Quantity must be a whole number\n- Rate must be a valid amount\n- {str(e)}")
            return

        pdf = InvoicePDF()
        pdf.add_page()
        pdf.add_buyer_details(name, phone, self.bill_counter)
        pdf.add_item_table(product, hsn, imei, qty, rate, 18.0, discount)
        pdf.add_footer()

        filename = os.path.join(BILLS_FOLDER, f"{name.replace(' ', '_')}_Bill_{self.bill_counter}.pdf")
        pdf.output(filename)
        
        try:
            webbrowser.open(filename)
        except:
            messagebox.showinfo("Invoice Saved", f"Invoice saved as:\n{filename}")
        
        # Clear form and increment counter
        self.clear_form()
        self.bill_counter += 1
        self.entry_bill_counter.delete(0, END)
        self.entry_bill_counter.insert(0, str(self.bill_counter))
        self.status_bar.config(text=f"Last bill generated: Bill #{self.bill_counter-1} - {name}")
    
    def clear_form(self):
        self.entry_name.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_product.delete(0, END)
        self.entry_hsn.delete(0, END)
        self.entry_imei.delete(0, END)
        self.entry_qty.delete(0, END)
        self.entry_rate.delete(0, END)
        self.entry_discount.delete(0, END)
        self.entry_discount.insert(0, "0")
        self.entry_delivery.delete(0, END)
        self.entry_name.focus()
    
    def save_settings(self):
        try:
            self.bill_counter = int(self.entry_bill_counter.get().strip())
            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bill number")

if __name__ == "__main__":
    root = Tk()
    app = InvoiceApp(root)
    root.mainloop()