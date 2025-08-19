from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.schemas import (
    InvoiceCreate, InvoiceRead, PaymentCreate, PaymentRead, 
    SubscriptionCreate, SubscriptionRead
)
from app.models.models import Invoice, Payment, Subscription, Customer
from routers.users import get_current_active_user, require_role
from app.core.database import db

router = APIRouter()

@router.post("/invoices/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoiceCreate,
    current_user = Depends(get_current_active_user)
):
    """Create a new invoice"""
    try:
        # Verify customer exists
        customer = await Customer.get_id(invoice.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        db_invoice = await Invoice.create(**invoice.dict())
        return db_invoice
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/invoices/", response_model=List[InvoiceRead])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
):
    """Get all invoices"""
    try:
        invoices = await Invoice.all_invoices()
        return invoices[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/invoices/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(
    invoice_id: str,
    current_user = Depends(get_current_active_user)
):
    """Get a specific invoice by ID"""
    try:
        invoice = await Invoice.get_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/invoices/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
    invoice_id: str,
    invoice_update: InvoiceCreate,
    current_user = Depends(get_current_active_user)
):
    """Update an invoice"""
    try:
        # Verify invoice exists
        existing_invoice = await Invoice.get_id(invoice_id)
        if not existing_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
            
        # Verify customer exists if customer_id is being updated
        if invoice_update.customer_id != existing_invoice.customer_id:
            customer = await Customer.get_id(invoice_update.customer_id)
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
        
        await Invoice.update(invoice_id, **invoice_update.dict())
        updated_invoice = await Invoice.get_id(invoice_id)
        return updated_invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/invoices/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: str,
    current_user = Depends(require_role("admin"))
):
    """Delete an invoice (admin only)"""
    try:
        invoice = await Invoice.get_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
            
        await Invoice.delete(invoice_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/payments/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    current_user = Depends(get_current_active_user)
):
    """Create a new payment"""
    try:
        # Verify invoice exists
        invoice = await Invoice.get_id(payment.invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        db_payment = await Payment.create(**payment.dict())
        return db_payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payments/", response_model=List[PaymentRead])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
):
    """Get all payments"""
    try:
        payments = await Payment.all_payments()
        return payments[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/subscriptions/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription: SubscriptionCreate,
    current_user = Depends(get_current_active_user)
):
    """Create a new subscription"""
    try:
        # Verify customer exists
        customer = await Customer.get_id(subscription.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        db_subscription = await Subscription.create(**subscription.dict())
        return db_subscription
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscriptions/", response_model=List[SubscriptionRead])
async def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
):
    """Get all subscriptions"""
    try:
        subscriptions = await Subscription.all_subscriptions()
        return subscriptions[skip:skip+limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/subscriptions/{subscription_id}/cancel", response_model=SubscriptionRead)
async def cancel_subscription(
    subscription_id: str,
    current_user = Depends(get_current_active_user)
):
    """Cancel a subscription"""
    try:
        # Verify subscription exists
        subscription = await Subscription.get_id(subscription_id)
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
            
        # Update status to cancelled
        await Subscription.update(subscription_id, status="cancelled")
        updated_subscription = await Subscription.get_id(subscription_id)
        return updated_subscription
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
