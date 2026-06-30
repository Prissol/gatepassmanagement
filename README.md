# Gate Pass Management System

A comprehensive, enterprise-grade gate pass management solution for Odoo 18.0 that provides complete tracking and management of material movements, visitor access, and vehicle entries/exits.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [User Roles & Permissions](#user-roles--permissions)
- [Usage Guide](#usage-guide)
  - [Material Gate Pass](#material-gate-pass)
  - [Visitor Gate Pass](#visitor-gate-pass)
  - [Vehicle Gate Pass](#vehicle-gate-pass)
- [Reports](#reports)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

## 🎯 Overview

The Gate Pass Management System is designed to streamline and automate the process of managing gate passes for materials, visitors, and vehicles. It provides a professional, international-standard solution with comprehensive tracking, approval workflows, and detailed reporting capabilities.

### Key Benefits

- **Complete Visibility**: Track all material movements, visitor entries, and vehicle access in one centralized system
- **Approval Workflow**: Implement proper authorization processes with role-based access control
- **Professional Documentation**: Generate branded PDF gate passes with all necessary information
- **Audit Trail**: Maintain complete history and tracking of all gate pass activities
- **Multi-Company Support**: Manage gate passes across multiple companies
- **Mobile-Friendly**: Access and manage gate passes from any device

## ✨ Features

### Material Gate Pass

- **Comprehensive Material Tracking**
  - Detailed item lists with quantity, unit of measure, and serial numbers
  - Item codes and descriptions
  - Remarks and notes for each item
  
- **Movement Types**
  - Material Outgoing
  - Material Incoming
  - Material Return
  - Internal Transfer

- **Approval Workflow**
  - Draft → Approved → Gate Out → Returned
  - Department manager approval required
  - Automatic status tracking

- **Transportation Details**
  - Vehicle registration number
  - Driver information (name, license, contact)
  - Expected return date tracking

- **Additional Features**
  - Supporting document attachments
  - Internal notes for authorized personnel
  - Complete audit trail

### Visitor Gate Pass

- **Visitor Information Management**
  - Full name, first name, last name
  - Email and phone number
  - Multiple ID types (National ID, Passport, Driving License, Company ID, Other)
  - ID number tracking

- **Visit Details**
  - Person to meet
  - Department to visit
  - Visit type (Business, Interview, Delivery, Maintenance, Inspection, Training, Other)
  - Purpose of visit
  - Expected duration

- **Check-In/Check-Out System**
  - Automatic time tracking
  - Duration calculation (hours)
  - Visitor badge number assignment
  - Vehicle information (if visitor brought a vehicle)

- **Tracking**
  - Real-time status (Checked In / Checked Out)
  - Gate officer assignment
  - Complete visit history

### Vehicle Gate Pass

- **Vehicle Information**
  - Registration number
  - Vehicle type (Truck, Pickup, Loader, Van, Car, SUV, Motorcycle, Bicycle, Bus, Trailer, Other)
  - Make, model, and color
  - Visit type classification

- **Driver Information**
  - Full name
  - License number
  - Contact number and email
  - Company/Organization

- **Cargo Tracking**
  - Material/cargo description
  - Purpose of visit
  - Duration tracking

- **Check-In/Check-Out**
  - Automatic time recording
  - Duration calculation
  - Gate officer tracking

### General Features

- **Role-Based Access Control**
  - Gate Pass Administrator (full access)
  - Department Manager (approval rights)
  - Gate Officer (processing rights)
  - Regular User (request creation)

- **Advanced Search & Filtering**
  - Search by reference, name, ID, phone, etc.
  - Filter by status, date, type
  - Group by various criteria
  - Quick filters (Today, This Week, This Month)

- **Professional Reports**
  - Company-branded PDF reports
  - Complete information display
  - Signature sections
  - Generation timestamp

- **Integration**
  - Mail integration with activity tracking
  - Chatter for communication
  - Multi-company support
  - HR integration (employees, departments)

## 📦 Installation

### Prerequisites

- Odoo 18.0 or later
- Required Odoo modules:
  - `base`
  - `mail`
  - `hr` (Human Resources)
  - `stock` (Inventory)

### Installation Steps

1. **Copy the Module**
   ```bash
   # Copy the gate_pass folder to your Odoo addons directory
   cp -r gate_pass /path/to/odoo/addons/
   ```

2. **Update Apps List**
   - Log in to Odoo as Administrator
   - Go to Apps menu
   - Click "Update Apps List"

3. **Install the Module**
   - Search for "Gate Pass Management" in Apps
   - Click "Install"

4. **Configure Security Groups** (Optional)
   - Go to Settings → Users & Companies → Groups
   - Assign users to appropriate groups:
     - Gate Pass Administrator
     - Department Manager
     - Gate Officer

## ⚙️ Configuration

### Sequence Configuration

The module automatically creates sequences for gate pass numbering:
- **Material Gate Pass**: MGP-0001, MGP-0002, ...
- **Visitor Gate Pass**: VGP-0001, VGP-0002, ...
- **Vehicle Gate Pass**: VHP-0001, VHP-0002, ...

To customize sequences:
1. Go to Settings → Technical → Sequences & Identifiers → Sequences
2. Search for "Gate Pass"
3. Modify prefix, padding, or numbering as needed

### Company Configuration

The module supports multi-company environments. Each gate pass is associated with a company, and reports will display company information automatically.

## 👥 User Roles & Permissions

### Gate Pass Administrator
- **Full Access**: Create, read, update, delete all gate passes
- **Reset to Draft**: Can reset cancelled gate passes to draft
- **Internal Notes**: Can view and edit internal notes
- **All Reports**: Access to all gate pass reports

### Department Manager
- **Approval Rights**: Can approve material gate passes
- **Full Access**: Create, read, update material gate passes in their department
- **Internal Notes**: Can view and edit internal notes
- **Reports**: Access to gate pass reports

### Gate Officer
- **Processing Rights**: Can process gate passes (check-in/check-out, mark as out/returned)
- **Create & Update**: Can create and update gate passes
- **No Delete**: Cannot delete gate passes
- **Reports**: Can print gate pass reports

### Regular User
- **Create Requests**: Can create gate pass requests
- **View Own**: Can view their own gate passes
- **Limited Update**: Can update their own draft gate passes
- **No Delete**: Cannot delete gate passes

## 📖 Usage Guide

### Material Gate Pass

#### Creating a Material Gate Pass

1. Navigate to **Gate Management → Material Gate Pass**
2. Click **Create**
3. Fill in the required information:
   - **Request Date**: Date and time of the request
   - **Movement Type**: Select the type of movement
   - **Requested By**: Automatically set to current user
   - **Department**: Select the department
   - **Purpose**: Enter detailed purpose for material movement
   - **Transportation Details**: Vehicle number, driver name, license, contact
   - **Expected Return Date**: If applicable

4. **Add Material Items**:
   - Click on "Material Items" tab
   - Click "Add a line"
   - Enter:
     - Item Description (required)
     - Item Code (optional)
     - Quantity (required)
     - Unit of Measure
     - Serial Number (if applicable)
     - Remarks

5. **Attach Documents** (optional):
   - Go to "Documents" tab
   - Upload supporting documents

6. Click **Save**

#### Approval Process

1. **Department Manager** reviews the gate pass
2. Click **Approve** (only visible for draft gate passes)
3. Gate pass status changes to "Approved"

#### Processing Gate Pass

1. **Gate Officer** processes the approved gate pass
2. Click **Mark as Gate Out** when material leaves
3. Click **Mark as Returned** when material returns
4. System automatically records timestamps

### Visitor Gate Pass

#### Creating a Visitor Gate Pass

1. Navigate to **Gate Management → Visitor Gate Pass**
2. Click **Create**
3. Fill in visitor information:
   - **Visitor Full Name** (required)
   - **Phone Number**
   - **Email Address**
   - **ID Type**: Select identification type
   - **ID Number**: Enter identification number
   - **Company/Organization**
   - **Company Address**

4. Enter visit details:
   - **Person to Meet** (required)
   - **Department to Visit**
   - **Visit Type**: Select type of visit
   - **Purpose of Visit** (required)
   - **Expected Duration**: In hours
   - **Visitor Badge Number**: If applicable

5. Vehicle information (if applicable):
   - Check "Vehicle Brought"
   - Enter vehicle registration number

6. Click **Save**

#### Check-In Process

1. Visitor arrives at gate
2. **Gate Officer** clicks **Check In**
3. System records check-in time
4. Status changes to "Checked In"

#### Check-Out Process

1. Visitor leaves
2. **Gate Officer** clicks **Check Out**
3. System records check-out time and calculates duration
4. Status changes to "Checked Out"

### Vehicle Gate Pass

#### Creating a Vehicle Gate Pass

1. Navigate to **Gate Management → Vehicle Gate Pass**
2. Click **Create**
3. Fill in vehicle information:
   - **Vehicle Registration Number** (required)
   - **Vehicle Type** (required)
   - **Vehicle Make**: e.g., Toyota, Honda
   - **Vehicle Model**: e.g., Corolla, Civic
   - **Vehicle Color**

4. Enter driver information:
   - **Driver Full Name** (required)
   - **License Number**
   - **Contact Number** (required)
   - **Email**
   - **Company/Organization**

5. Enter visit details:
   - **Visit Type**: Delivery, Pickup, Service, etc.
   - **Cargo/Material Description**
   - **Purpose**
   - **Expected Duration**: In hours

6. Click **Save**

#### Processing Vehicle Gate Pass

1. **Gate Officer** processes vehicle entry
2. Click **Check In** when vehicle enters
3. Click **Check Out** when vehicle leaves
4. System automatically calculates duration

## 📄 Reports

### Generating Reports

All gate passes can be printed as professional PDF reports:

1. Open any gate pass record
2. Click the **Print** button (top right)
3. Report will be generated with:
   - Company information and branding
   - Complete gate pass details
   - All relevant information
   - Signature sections
   - Generation timestamp

### Report Features

- **Company Branding**: Automatically includes company name, address, and country
- **Color-Coded Sections**: Professional layout with color-coded headers
- **Complete Information**: All relevant details included
- **Signature Sections**: Space for required signatures
- **Timestamp**: Generation date and time included

## 🔧 Technical Details

### Module Structure

```
gate_pass/
├── __init__.py
├── __manifest__.py
├── README.md
├── data/
│   └── sequence_data.xml
├── models/
│   ├── __init__.py
│   ├── material_pass.py
│   ├── visitor_pass.py
│   └── vehicle_pass.py
├── reports/
│   ├── material_pass_report.xml
│   ├── visitor_pass_report.xml
│   └── vehicle_pass_report.xml
├── security/
│   ├── security_groups.xml
│   └── ir.model.access.csv
└── views/
    ├── material_pass_views.xml
    ├── visitor_pass_views.xml
    ├── vehicle_pass_views.xml
    └── menu.xml
```

### Models

- **gate.material.pass**: Material gate pass records
- **gate.material.pass.line**: Material items in gate passes
- **gate.visitor.pass**: Visitor gate pass records
- **gate.vehicle.pass**: Vehicle gate pass records

### Dependencies

- `base`: Core Odoo functionality
- `mail`: Email and messaging features
- `hr`: Human Resources (for employees and departments)
- `stock`: Inventory management

### Database Fields

Key fields include:
- Automatic sequence numbering
- Status tracking with workflow
- Timestamp fields for all state changes
- Related fields for user and company information
- Computed fields for duration calculations

## 🐛 Troubleshooting

### Common Issues

#### Issue: "No matching record found for external id" during installation

**Solution**: Ensure the module files are in the correct directory and the module name in `__manifest__.py` matches the folder name.

#### Issue: Cannot approve material gate pass

**Solution**: 
1. Verify user is assigned to "Department Manager" group
2. Check that gate pass is in "Draft" status
3. Ensure material items are added

#### Issue: Reports not generating

**Solution**:
1. Check that report templates are properly installed
2. Verify user has print permissions
3. Check browser console for JavaScript errors

#### Issue: Sequence numbers not generating

**Solution**:
1. Go to Settings → Technical → Sequences
2. Verify sequences exist for gate passes
3. Check sequence configuration (prefix, padding)

### Migration Issues

If upgrading from a previous version:

1. **visitor_phone field**: The `visitor_phone` field is optional to maintain backward compatibility. Existing records may have NULL values.

2. **Field Changes**: Some field names have changed. The system maintains backward compatibility where possible.

## 📞 Support

### Getting Help

- **Documentation**: Refer to this README for detailed information
- **Odoo Community**: Visit [Odoo Community Forum](https://www.odoo.com/forum)
- **Technical Support**: Contact your system administrator

### Reporting Issues

When reporting issues, please include:
- Odoo version
- Module version
- Steps to reproduce
- Error messages (if any)
- Screenshots (if applicable)

## 📝 Version History

### Version 18.0.1.0.6
- Enhanced models with international fields
- Professional report templates
- Improved UI/UX
- Multi-company support
- Comprehensive documentation

### Previous Versions
- Initial release with basic gate pass functionality

## 📜 License

This module is licensed under LGPL-3.

## 👨‍💻 Author

**PPM**

## 🌐 Website

https://www.odoo.com

---

**Note**: This module is designed for Odoo 18.0. Ensure compatibility before installation in other versions.

